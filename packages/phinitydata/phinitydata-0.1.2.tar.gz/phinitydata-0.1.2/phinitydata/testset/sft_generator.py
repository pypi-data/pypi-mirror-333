"""
SFT data generation module with document grounding and instruction evolution.
Focused on generating high-quality instruction-response pairs for supervised fine-tuning.
"""

import random
import json
import os
import time
from typing import List, Dict, Union, Optional, Any, Tuple, Literal

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.prompts import ChatPromptTemplate
import chromadb
import openai

class SFTGenerator:
    """
    Generates SFT data using evolution and document-based verification.
    Uses a "evolve-then-verify" approach for better document grounding.
    """
    
    def __init__(self, 
                api_key: Optional[str] = None,
                llm_model: str = "gpt-4o-mini",
                embedding_model: Optional[Embeddings] = None,
                vector_store_type: str = "faiss",
                temperature: float = 0.7):
        """
        Initialize SFT Generator with models and strategies.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY environment variable
            llm_model: Model to use for generation (default: gpt-4o-mini)
            embedding_model: Optional custom embedding model
            vector_store_type: Type of vector store to use ("faiss" or "chroma")
            temperature: Temperature for generation (default: 0.7)
        """
        # Set up API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided either through api_key parameter "
                "or OPENAI_API_KEY environment variable"
            )
        
        # Initialize OpenAI client
        try:
            self.llm = ChatOpenAI(
                api_key=self.api_key,
                model=llm_model, 
                temperature=temperature
            )
            self.embedding_model = embedding_model or OpenAIEmbeddings(api_key=self.api_key)
        except openai.OpenAIError as e:
            raise ValueError(f"Error initializing OpenAI client: {str(e)}")
            
        self.evolution_strategies = self._load_evolution_strategies()
        self.question_history = []  # Track generated questions to prevent repetition
        self.vector_store_type = vector_store_type.lower()
        
    def generate(
        self,
        seed_instructions: List[str],
        documents: Optional[List[str]] = None,
        target_samples: int = 10,
        domain_context: str = "",
        evolution_config: Optional[Dict] = None,
        strict_grounding: bool = False,
        verbose: bool = False,
        export_format: Literal["json", "jsonl"] = "json",
        export_path: Optional[str] = None
    ) -> Dict:
        """Generate instruction-response pairs, evolving from seeds to create a population."""
        results = []
        doc_store = self._create_document_store(documents) if documents else None
        
        if verbose:
            print("\n=== Starting Instruction Generation ===")
            print(f"Seeds: {len(seed_instructions)}")
            print(f"Target samples: {target_samples}")
        
        # Initialize population with seed instructions
        population = seed_instructions.copy()
        used_indices = set()
        
        while len(results) < target_samples:
            # Loop through population in order
            for i, current in enumerate(population):
                if len(results) >= target_samples:
                    break
                
                # Skip if we've already used this population member
                if i in used_indices:
                    continue
                
                # Select strategy
                strategy = self._select_strategy(evolution_config)
                
                if verbose:
                    print(f"\nEvolving with {strategy}:")
                    print(f"Parent: {current}")
                
                # Get relevant docs for context
                if doc_store:
                    _, relevant_docs = self._find_relevant_docs(current, doc_store)
                    doc_context = "\n".join(relevant_docs)
                else:
                    doc_context = ""
                    relevant_docs = []
                
                # Evolve to create new instruction
                new_instruction = self._evolve_instruction(
                    current,
                    strategy,
                    domain_context,
                    self.question_history,
                    doc_context
                )
                
                # Verify if needed
                if strict_grounding and documents:
                    is_answerable, relevant_docs = self._verify_answerability(new_instruction, doc_store)
                    if not is_answerable:
                        continue
                
                # Generate response
                response = self._generate_response(new_instruction, relevant_docs, domain_context)
                
                # Add to results and population
                results.append({
                    "instruction": new_instruction,
                    "response": response,
                    "parent": current,
                    "strategy": strategy,
                    "relevant_documents": relevant_docs,
                    "metadata": {
                        "strategy": strategy,
                        "parent": current,
                        "grounding_type": "strict" if strict_grounding else "flexible"
                    }
                })
                population.append(new_instruction)
                used_indices.add(i)
                
                if verbose:
                    print(f"New instruction: {new_instruction}")
                    print(f"Response preview: {response[:200]}...")
                    print("-" * 80)
            
            # Reset used_indices if needed
            if len(results) < target_samples and len(used_indices) == len(population):
                used_indices.clear()
        
        # Structure final results
        final_results = {
            "samples": results,
            "metrics": {
                "seeds_used": len(seed_instructions),
                "evolved": len(results),
                "answerable": len([r for r in results if r.get("answerable", True)]),
                "final": len(results)
            }
        }
        
        # Export if path provided
        if export_path:
            self._export_results(final_results, export_path, export_format)
        
        return final_results
    
    def _create_document_store(self, documents: List[str]) -> VectorStore:
        """Create a vector store from documents for similarity search."""
        doc_objects = [Document(page_content=doc) for doc in documents]
        
        if self.vector_store_type == "chroma":
            # Use ChromaDB
            client = chromadb.Client()
            # Create a unique collection name
            collection_name = f"sft_gen_{hash(str(documents)[:100])}"
            return Chroma.from_documents(
                documents=doc_objects, 
                embedding=self.embedding_model,
                collection_name=collection_name
            )
        else:
            # Default to FAISS
            return FAISS.from_documents(doc_objects, self.embedding_model)
    
    def _verify_answerability(self, instruction: str, doc_store: VectorStore) -> Tuple[bool, List[str]]:
        """Check if an instruction is answerable from the document set."""
        # Retrieve relevant documents
        results = doc_store.similarity_search(instruction, k=3)
        relevant_texts = [doc.page_content for doc in results]
        
        # Use LLM to verify answerability
        prompt = ChatPromptTemplate.from_template("""
        Determine if the following instruction can be answered using ONLY the provided context.
        
        INSTRUCTION: {instruction}
        
        CONTEXT:
        {context}
        
        Can this instruction be answered completely using only the information in the context?
        Answer YES or NO, then explain your reasoning.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "instruction": instruction,
            "context": "\n".join(relevant_texts)
        }).content
        
        is_answerable = "YES" in response.split("\n")[0].upper()
        
        return is_answerable, relevant_texts
        
    def _repair_instruction(self, instruction: str, relevant_docs: List[str], domain_context: str) -> str:
        """Modify an instruction to make it answerable from documents."""
        prompt = ChatPromptTemplate.from_template("""
        Modify the following instruction to make it answerable using ONLY the provided context.
        The modified instruction should:
        1. Be answerable completely from the context
        2. Maintain the same general intent and complexity
        3. Be specific and clear
        
        DOMAIN: {domain}
        
        ORIGINAL INSTRUCTION: {instruction}
        
        AVAILABLE CONTEXT:
        {context}
        
        MODIFIED INSTRUCTION:
        """)
        
        chain = prompt | self.llm
        return chain.invoke({
            "domain": domain_context,
            "instruction": instruction,
            "context": "\n".join(relevant_docs)
        }).content.strip()
    
    def _evolve_instruction(self, 
                           instruction: str, 
                           strategy: str, 
                           domain_context: str,
                           history: List[str],
                           document_context: str = "") -> str:
        """
        Evolve an instruction using the specified strategy.
        
        Args:
            instruction: Original instruction to evolve
            strategy: Evolution strategy to apply
            domain_context: Domain context for guidance
            history: Previous questions to avoid repetition
            document_context: Available document context for grounding
            
        Returns:
            Evolved instruction
        """
        prompt_template = self.evolution_strategies[strategy]["prompt_template"]
        
        # Add length information
        original_length = len(instruction.split())
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm
        
        evolved = chain.invoke({
            "original_prompt": instruction,
            "domain_summary": domain_context,
            "recent_history": "\n".join(history[-3:]),  # Last 3 instructions
            "document_context": document_context,
            "original_length": original_length
        }).content.strip()
        
        # Remove any "Revised Prompt:" prefix
        if evolved.startswith("Revised Prompt:"):
            evolved = evolved.replace("Revised Prompt:", "").strip()
        
        return evolved
    
    def _generate_response(self, instruction: str, relevant_docs: List[str], domain_context: str) -> str:
        """Generate a response to an instruction grounded in documents."""
        prompt = ChatPromptTemplate.from_template("""
        You are an expert responding to questions in the following domain:
        {domain}
        
        Please respond to the following instruction using ONLY information from the provided context.
        Be thorough, accurate, and helpful in your response.
        
        INSTRUCTION: {instruction}
        
        CONTEXT:
        {context}
        
        YOUR RESPONSE:
        """)
        
        # Use _get_completion internally
        formatted_prompt = prompt.format(
            domain=domain_context,
            instruction=instruction,
            context="\n".join(relevant_docs) if relevant_docs else "No specific context provided."
        )
        return self._get_completion(formatted_prompt)
    
    def _select_strategy(self, config: Dict) -> str:
        """Select evolution strategy based on weights."""
        strategies = config.get("strategies", ["deepening", "concretizing", "reasoning"])
        weights = config.get("weights", [0.3, 0.4, 0.3])
        return random.choices(strategies, weights=weights)[0]
    
    def _load_evolution_strategies(self) -> Dict:
        """Load default evolution strategies with length control."""
        return {
            "deepening": {
                "description": "Makes instruction more detailed while maintaining length",
                "prompt_template": """
                Create a more specific version of the given prompt.
                The evolved prompt should:
                1. Add specific details or requirements THAT CAN BE ANSWERED from the document context
                2. Maintain similar length to the original prompt (within 20% longer/shorter)
                3. Keep the core intent clear and focused
                4. NOT introduce elements that aren't supported by the document context
                5. Return ONLY the evolved prompt without any prefix
                
                DOMAIN CONTEXT: {domain_summary}
                ORIGINAL PROMPT: {original_prompt}
                LENGTH GUIDE: Keep close to {original_length} words
                
                RECENT INSTRUCTIONS (avoid repeating these):
                {recent_history}
                
                Create a focused, specific version:
                """
            },
            "concretizing": {
                "description": "Adds concrete examples while maintaining length",
                "prompt_template": """
                Create a version with concrete examples that are answerable from the document context.
                The evolved prompt should:
                1. Include specific examples from the document context
                2. Maintain similar length to the original prompt (within 20% longer/shorter)
                3. Keep the core question clear and focused
                4. NOT add unnecessary complexity
                5. Return ONLY the evolved prompt without any prefix
                
                DOMAIN CONTEXT: {domain_summary}
                ORIGINAL PROMPT: {original_prompt}
                LENGTH GUIDE: Keep close to {original_length} words
                
                RECENT INSTRUCTIONS (avoid repeating these):
                {recent_history}
                
                Create a version with concrete examples:
                """
            },
            "reasoning": {
                "description": "Asks for reasoning or step-by-step explanations",
                "prompt_template": """
                Rewrite the given prompt to focus on reasoning or explanations.
                The evolved prompt should:
                1. Ask for step-by-step explanations
                2. Request reasoning behind concepts
                3. Maintain the core intent of the original prompt
                4. Return ONLY the evolved prompt without any prefix like "Revised Prompt:"
                
                DOMAIN CONTEXT: {domain_summary}
                ORIGINAL PROMPT: {original_prompt}
                
                RECENT INSTRUCTIONS (avoid repeating these):
                {recent_history}
                
                Create a version that focuses on reasoning:
                """
            },
            "comparative": {
                "description": "Transforms the prompt to include comparison elements",
                "prompt_template": """
                Rewrite the given prompt to include comparative analysis.
                The evolved prompt should:
                1. Ask to compare or contrast related concepts
                2. Include evaluation of different approaches or perspectives
                3. Maintain the core intent of the original prompt
                4. Return ONLY the evolved prompt without any prefix like "Revised Prompt:"
                
                DOMAIN CONTEXT: {domain_summary}
                ORIGINAL PROMPT: {original_prompt}
                
                RECENT INSTRUCTIONS (avoid repeating these):
                {recent_history}
                
                Create a version with comparative elements:
                """
            }
        }
    
    def _check_partial_answerability(self, instruction: str, doc_store: VectorStore) -> Tuple[bool, List[str]]:
        """More lenient verification that checks if parts of instruction are answerable."""
        # Retrieve relevant documents
        results = doc_store.similarity_search(instruction, k=5)  # Get more documents
        relevant_texts = [doc.page_content for doc in results]
        
        # Use LLM to verify answerability with lower bar
        prompt = ChatPromptTemplate.from_template("""
        Determine if the following instruction can be at least PARTIALLY answered using the provided context.
        
        INSTRUCTION: {instruction}
        
        CONTEXT:
        {context}
        
        Even if the instruction cannot be FULLY answered, can the main parts or key aspects be addressed?
        Be lenient in your assessment - if the core question can be answered, consider it answerable.
        
        Answer YES or NO, then explain your reasoning.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "instruction": instruction,
            "context": "\n".join(relevant_texts)
        }).content
        
        is_answerable = "YES" in response.split("\n")[0].upper()
        
        return is_answerable, relevant_texts
    
    def _simplify_instruction(self, instruction: str, previous_version: str, context: List[str]) -> str:
        """Simplify an instruction to make it more likely to be answerable."""
        prompt = ChatPromptTemplate.from_template("""
        The following instruction has become too complex to be answered from the available context.
        
        COMPLEX INSTRUCTION: {complex_instruction}
        
        PREVIOUS SIMPLER VERSION: {previous_version}
        
        AVAILABLE CONTEXT:
        {context}
        
        Please simplify this instruction while preserving its core intent. The simplified instruction should:
        1. Focus only on key aspects that can be answered from the context
        2. Remove unnecessary details, scenarios, or requirements
        3. Be clear and straightforward
        4. Be answerable from the given context
        
        SIMPLIFIED INSTRUCTION:
        """)
        
        chain = prompt | self.llm
        return chain.invoke({
            "complex_instruction": instruction,
            "previous_version": previous_version,
            "context": "\n".join(context)
        }).content.strip()
    
    def _get_all_document_content(self, documents: List[str]) -> List[str]:
        """Return all document content as a list."""
        return documents 

    def add_evolution_strategy(self,
                              name: str,
                              description: str,
                              prompt_template: str) -> None:
        """
        Add a custom evolution strategy to the generator.
        
        Args:
            name: Unique name for the strategy
            description: Description of what the strategy does
            prompt_template: Template for evolving prompts with {original_prompt},
                            {domain_summary}, {recent_history}, and optional {document_context} placeholders
        """
        self.evolution_strategies[name] = {
            "description": description,
            "prompt_template": prompt_template
        } 

    def _export_results(self, results: Dict, path: str, format: str = "json"):
        """
        Export results to file
        
        Args:
            results: Results dictionary to export
            path: Path to export file
            format: Export format ("json" or "jsonl")
        """
        if not path:
            return
        
        # Create directory if path contains directories
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        if format == "json":
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
        elif format == "jsonl":
            with open(path, 'w', encoding='utf-8') as f:
                for sample in results['samples']:
                    f.write(json.dumps(sample) + '\n')

    def _verify_instruction(self, instruction: str, docs: List[str] = []) -> bool:
        """
        Verify if an instruction is answerable and high-quality
        
        Args:
            instruction: Instruction to verify
            docs: Optional documents for grounding
            
        Returns:
            Boolean indicating if instruction is valid
        """
        # When no docs provided, verify based on general criteria:
        # 1. Instruction is clear and well-formed
        # 2. Task is achievable with general knowledge
        # 3. Response can be evaluated
        
        prompt = f"""Please verify if this instruction is clear, answerable, and high-quality:
        
Instruction: {instruction}

Verification criteria:
1. The instruction is clear and unambiguous
2. The task can be completed with general knowledge (no special documents needed)
3. The expected response format is clear
4. The instruction promotes thoughtful, detailed responses
5. The task is appropriate and ethical

Respond with YES if it meets all criteria, or NO with a brief explanation if it fails any criterion."""

        response = self._get_completion(prompt)
        return response.strip().startswith("YES") 

    def _get_completion(self, prompt: str) -> str:
        """
        Get completion from LLM with error handling
        
        Args:
            prompt: Prompt to send to LLM
            
        Returns:
            Generated completion text
        """
        try:
            # Create prompt template
            prompt_template = ChatPromptTemplate.from_template("{input}")
            
            # Create chain
            chain = prompt_template | self.llm
            
            # Get response
            response = chain.invoke({"input": prompt})
            
            return response.content.strip()
            
        except Exception as e:
            print(f"Error getting completion: {str(e)}")
            # Return empty string or raise exception depending on your error handling preference
            return "" 

    def _find_relevant_docs(self, instruction: str, doc_store: Optional[VectorStore]) -> Tuple[bool, List[str]]:
        """
        Find documents relevant to the instruction without strict answerability requirements.
        
        Args:
            instruction: The instruction to find relevant docs for
            doc_store: Vector store containing the documents
            
        Returns:
            Tuple of (True, relevant_docs)
        """
        if not doc_store:
            return True, []
        
        # Use similarity search to find relevant documents
        relevant_docs = doc_store.similarity_search(instruction, k=3)
        return True, [doc.page_content for doc in relevant_docs] 