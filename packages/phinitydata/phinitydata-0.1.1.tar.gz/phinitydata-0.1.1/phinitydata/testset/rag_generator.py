"""
Test set generation module wrapping around Ragas TestsetGenerator.
Provides customized test generation capabilities.
"""

from typing import List, Dict, Union, Optional, Any
import os

from ragas.testset import TestsetGenerator as RagasGenerator
from ragas.testset.graph import KnowledgeGraph, Node, NodeType
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from ..connectors.base import BaseConnector
from .models import Testset, QAPair


class TestsetGenerator:
    """
    Wrapper around Ragas TestsetGenerator with additional functionality - this is knowledge graph construction from documents/QA generation from documents.
    """

    def __init__(self, llm=None, embedding_model=None):
        """
        Initialize the test set generator.

        Args:
            llm: Optional LLM to use for generation (defaults to gpt-4o-mini)
            embedding_model: Optional embedding model
        """
        # Default to OpenAI if no models provided
        self.llm = llm or LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
        self.embedding_model = embedding_model or LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    def _create_query_distribution(self, query_distribution: Dict[str, float] = None):
        """
        Convert simplified distribution format to Ragas format.

        Args:
            query_distribution: Dictionary mapping query types to their probabilities

        Returns:
            List of tuples containing (QuerySynthesizer, probability)
        """
        from ragas.testset.synthesizers import (
            SingleHopSpecificQuerySynthesizer,
            MultiHopAbstractQuerySynthesizer,
            MultiHopSpecificQuerySynthesizer
        )
        
        # Default distribution if none provided
        if not query_distribution:
            return [
                (SingleHopSpecificQuerySynthesizer(llm=self.llm), 0.5),
                (MultiHopAbstractQuerySynthesizer(llm=self.llm), 0.25),
                (MultiHopSpecificQuerySynthesizer(llm=self.llm), 0.25),
            ]
        
        # Convert simplified format to Ragas format
        distribution = []
        if "single_hop_specific" in query_distribution:
            distribution.append(
                (SingleHopSpecificQuerySynthesizer(llm=self.llm), 
                 query_distribution["single_hop_specific"])
            )
        if "multi_hop_abstract" in query_distribution:
            distribution.append(
                (MultiHopAbstractQuerySynthesizer(llm=self.llm), 
                 query_distribution["multi_hop_abstract"])
            )
        if "multi_hop_specific" in query_distribution:
            distribution.append(
                (MultiHopSpecificQuerySynthesizer(llm=self.llm), 
                 query_distribution["multi_hop_specific"])
            )
            
        return distribution

    def generate_from_documents(
        self, 
        documents: List[str],
        testset_size: int = 10,
        query_distribution: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> Testset:
        """
        Generate QA pairs from documents.

        Args:
            documents: List of document paths or content
            testset_size: Number of QA pairs to generate
            query_distribution: Distribution of question types
            **kwargs: Additional arguments for generation

        Returns:
            Testset object containing generated QA pairs
        """
        # Load documents using langchain
        from langchain_community.document_loaders import TextLoader
        
        langchain_docs = []
        for doc in documents:
            if os.path.isfile(doc):
                loader = TextLoader(doc)
                langchain_docs.extend(loader.load())
            else:
                # Treat as raw text
                langchain_docs.append(Document(page_content=doc))
        
        # Create Ragas generator
        ragas_generator = RagasGenerator(
            llm=self.llm,
            embedding_model=self.embedding_model
        )
        
        # Generate testset using Ragas
        distribution = self._create_query_distribution(query_distribution)
        ragas_dataset = ragas_generator.generate_with_langchain_docs(
            langchain_docs,
            testset_size=testset_size,
            query_distribution=distribution
        )
        
        # Convert Ragas dataset to our format
        return self._convert_ragas_to_testset(ragas_dataset)

    def generate_from_connector(
        self,
        connector: BaseConnector,
        testset_size: int = 10,
        query_distribution: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> Testset:
        """
        Generate QA pairs from a data connector.

        Args:
            connector: Data source connector
            testset_size: Number of QA pairs to generate
            query_distribution: Distribution of question types
            **kwargs: Additional arguments for generation

        Returns:
            Testset object containing generated QA pairs
        """
        # Get documents from connector
        docs, metadata = connector.get_documents()
        
        # Convert to langchain Document objects
        langchain_docs = []
        for i, doc in enumerate(docs):
            meta = metadata[i] if i < len(metadata) else {}
            langchain_docs.append(Document(page_content=doc, metadata=meta))
        
        # Create knowledge graph
        kg = KnowledgeGraph()
        for doc in langchain_docs:
            kg.nodes.append(
                Node(
                    type=NodeType.DOCUMENT,
                    properties={
                        "page_content": doc.page_content,
                        "document_metadata": doc.metadata
                    }
                )
            )
        
        # Apply transformations
        from ragas.testset.transforms import default_transforms, apply_transforms
        
        trans = default_transforms(
            documents=langchain_docs,  # Pass langchain Document objects
            llm=self.llm, 
            embedding_model=self.embedding_model
        )
        apply_transforms(kg, trans)
        
        # Create Ragas generator with knowledge graph
        ragas_generator = RagasGenerator(
            llm=self.llm,
            embedding_model=self.embedding_model,
            knowledge_graph=kg
        )
        
        # Generate testset using Ragas
        distribution = self._create_query_distribution(query_distribution)
        ragas_dataset = ragas_generator.generate(
            testset_size=testset_size,
            query_distribution=distribution
        )
        
        # Convert Ragas dataset to our format
        return self._convert_ragas_to_testset(ragas_dataset)

    def _convert_ragas_to_testset(self, ragas_dataset: Any) -> Testset:
        """
        Convert Ragas dataset format to our Testset format.

        Args:
            ragas_dataset: Dataset from Ragas generator

        Returns:
            Testset object with our format
        """
        # Convert to pandas for easier handling
        df = ragas_dataset.to_pandas()
        
        # Create QAPair objects from the dataframe
        qa_pairs = []
        for _, row in df.iterrows():
            # Create a dict from row for easier access
            row_dict = row.to_dict()
            
            qa_pairs.append(
                QAPair(
                    question=row_dict.get("user_input", ""),
                    answer=row_dict.get("reference", ""),
                    context=row_dict.get("reference_contexts", []),
                    metadata={
                        "type": row_dict.get("synthesizer_name", "unknown"),
                        "difficulty": "medium"  # Default since Ragas doesn't provide this
                    }
                )
            )
        
        return Testset(
            qa_pairs=qa_pairs,
            metadata={
                "size": len(qa_pairs),
                "generator_config": {
                    "llm": str(self.llm),
                    "embedding_model": str(self.embedding_model)
                }
            }
        ) 