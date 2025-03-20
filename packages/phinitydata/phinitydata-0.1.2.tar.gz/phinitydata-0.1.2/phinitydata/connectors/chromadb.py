from typing import Tuple, List, Dict, Any, Optional

from .base import BaseConnector


class ChromaDBConnector(BaseConnector):
    """Connector for ChromaDB collections."""
    
    def __init__(self, collection):
        """Initialize ChromaDB connector.
        
        Args:
            collection: ChromaDB collection object
        """
        self.collection = collection
    
    def get_documents(self) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Get documents and metadata from ChromaDB collection.
        
        Returns:
            Tuple of (documents, metadata)
        """
        results = self.collection.get(include=["documents", "metadatas"])
        documents = results.get("documents", [])
        metadatas = results.get("metadatas", [None] * len(documents))
        
        # Replace None with empty dict in metadatas
        metadatas = [m or {} for m in metadatas]
        
        return documents, metadatas
    
    def get_embeddings(self) -> Optional[List[List[float]]]:
        """Get embeddings from ChromaDB collection.
        
        Returns:
            List of embeddings or None if not available
        """
        try:
            results = self.collection.get(include=["embeddings"])
            return results.get("embeddings")
        except:
            return None