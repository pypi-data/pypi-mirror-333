from typing import List, Dict, Union, Optional
import os

from .testset.rag_generator import TestsetGenerator
from .connectors.base import BaseConnector


class Client:
    """Main Phinity client for synthetic data generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Phinity client.
        
        Args:
            api_key: API key for Phinity services. If not provided, 
                     will look for PHINITY_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("PHINITY_API_KEY")
        self.generator = TestsetGenerator()
    
    def generate_from_documents(
        self, 
        documents: List[str],
        testset_size: int = 10,
        query_distribution: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        """Generate QA pairs from documents.
        
        Args:
            documents: List of document paths or content
            testset_size: Number of QA pairs to generate
            query_distribution: Distribution of question types
            
        Returns:
            Testset object containing generated QA pairs
        """
        return self.generator.generate_from_documents(
            documents=documents,
            testset_size=testset_size,
            query_distribution=query_distribution,
            **kwargs
        )
    
    def generate_from_connector(
        self,
        connector: BaseConnector,
        testset_size: int = 10,
        query_distribution: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        """Generate QA pairs from a data connector.
        
        Args:
            connector: Data source connector
            testset_size: Number of QA pairs to generate
            query_distribution: Distribution of question types
            
        Returns:
            Testset object containing generated QA pairs
        """
        return self.generator.generate_from_connector(
            connector=connector,
            testset_size=testset_size,
            query_distribution=query_distribution,
            **kwargs
        )