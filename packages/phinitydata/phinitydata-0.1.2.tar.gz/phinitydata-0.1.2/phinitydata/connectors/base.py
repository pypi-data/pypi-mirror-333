from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Any, Optional


class BaseConnector(ABC):
    """Base class for data source connectors."""
    
    @abstractmethod
    def get_documents(self) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Get documents and metadata from the data source.
        
        Returns:
            Tuple of (documents, metadata)
        """
        pass
    
    def get_embeddings(self) -> Optional[List[List[float]]]:
        """Get embeddings if available from the data source.
        
        Returns:
            List of embeddings or None if not available
        """
        return None