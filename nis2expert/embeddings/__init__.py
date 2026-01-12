"""
Embeddings management for NIS-2 documents.

This module provides a unified interface for generating and managing embeddings
for document retrieval and semantic search.
"""

from typing import List, Optional

from langchain_openai import OpenAIEmbeddings


class NIS2Embeddings:
    """
    Embeddings manager for NIS-2/ENISA documents.
    
    Provides a consistent interface for generating embeddings using various
    embedding models, with caching and optimization for compliance documents.
    """
    
    def __init__(
        self,
        model: Optional[str] = None,
        openai_api_key: Optional[str] = None,
    ):
        """
        Initialize the embeddings manager.
        
        Args:
            model: Embedding model to use
            openai_api_key: OpenAI API key
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.model = model or settings.embedding_model
        self.api_key = openai_api_key or settings.openai_api_key
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set NIS2_OPENAI_API_KEY environment variable "
                "or provide it in .env file"
            )
        
        self.embeddings = OpenAIEmbeddings(
            model=self.model,
            openai_api_key=self.api_key,
        )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)
    
    def get_embeddings(self):
        """
        Get the underlying embeddings object for use with vector stores.
        
        Returns:
            Embeddings object compatible with LangChain vector stores
        """
        return self.embeddings


def get_embeddings(
    model: Optional[str] = None,
    openai_api_key: Optional[str] = None,
) -> OpenAIEmbeddings:
    """
    Factory function to get embeddings instance.
    
    Args:
        model: Embedding model to use
        openai_api_key: OpenAI API key
        
    Returns:
        OpenAI embeddings instance
    """
    embeddings_manager = NIS2Embeddings(model=model, openai_api_key=openai_api_key)
    return embeddings_manager.get_embeddings()
