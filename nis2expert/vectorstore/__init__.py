"""
Vector store management for NIS-2 document retrieval.

This module provides a unified interface for vector stores (Chroma, FAISS)
with persistence and retrieval capabilities optimized for compliance documents.
"""

from pathlib import Path
from typing import List, Optional, Union

from langchain.schema import Document
from langchain_community.vectorstores import Chroma, FAISS


class NIS2VectorStore:
    """
    Vector store manager for NIS-2/ENISA documents.
    
    Provides a unified interface for creating, persisting, and querying
    vector stores for document retrieval.
    """
    
    SUPPORTED_STORES = {"chroma", "faiss"}
    
    def __init__(
        self,
        store_type: Optional[str] = None,
        persist_directory: Optional[Union[str, Path]] = None,
        collection_name: Optional[str] = None,
    ):
        """
        Initialize the vector store manager.
        
        Args:
            store_type: Type of vector store ('chroma' or 'faiss')
            persist_directory: Directory for persisting the vector store
            collection_name: Name of the collection/index
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.store_type = (store_type or settings.vectorstore_type).lower()
        self.persist_directory = Path(persist_directory) if persist_directory else settings.vectorstore_dir
        self.collection_name = collection_name or settings.collection_name
        
        if self.store_type not in self.SUPPORTED_STORES:
            raise ValueError(
                f"Unsupported vector store type: {self.store_type}. "
                f"Supported types: {', '.join(self.SUPPORTED_STORES)}"
            )
        
        self.vectorstore = None
    
    def create_vectorstore(
        self,
        documents: List[Document],
        embeddings,
    ):
        """
        Create a new vector store from documents.
        
        Args:
            documents: List of documents to index
            embeddings: Embeddings instance
            
        Returns:
            Vector store instance
        """
        if self.store_type == "chroma":
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=str(self.persist_directory),
                collection_name=self.collection_name,
            )
        elif self.store_type == "faiss":
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=embeddings,
            )
            # Persist FAISS index
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            index_path = self.persist_directory / f"{self.collection_name}.faiss"
            self.vectorstore.save_local(str(index_path))
        
        return self.vectorstore
    
    def load_vectorstore(self, embeddings):
        """
        Load an existing vector store from disk.
        
        Args:
            embeddings: Embeddings instance
            
        Returns:
            Vector store instance
        """
        if self.store_type == "chroma":
            self.vectorstore = Chroma(
                persist_directory=str(self.persist_directory),
                embedding_function=embeddings,
                collection_name=self.collection_name,
            )
        elif self.store_type == "faiss":
            index_path = self.persist_directory / f"{self.collection_name}.faiss"
            if not index_path.exists():
                raise FileNotFoundError(
                    f"FAISS index not found at {index_path}. "
                    "Create a new vector store first."
                )
            self.vectorstore = FAISS.load_local(
                str(index_path),
                embeddings,
                allow_dangerous_deserialization=True,
            )
        
        return self.vectorstore
    
    def add_documents(self, documents: List[Document]):
        """
        Add documents to an existing vector store.
        
        Args:
            documents: List of documents to add
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        self.vectorstore.add_documents(documents)
        
        # Persist changes for FAISS
        if self.store_type == "faiss":
            index_path = self.persist_directory / f"{self.collection_name}.faiss"
            self.vectorstore.save_local(str(index_path))
    
    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None,
    ) -> List[Document]:
        """
        Perform similarity search in the vector store.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        from nis2expert.config import get_settings
        settings = get_settings()
        k = k or settings.retrieval_k
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def similarity_search_with_score(
        self,
        query: str,
        k: Optional[int] = None,
    ) -> List[tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query: Query text
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        from nis2expert.config import get_settings
        settings = get_settings()
        k = k or settings.retrieval_k
        
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def as_retriever(self, **kwargs):
        """
        Get the vector store as a retriever for use in chains.
        
        Args:
            **kwargs: Additional arguments for retriever configuration
            
        Returns:
            Retriever instance
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        from nis2expert.config import get_settings
        settings = get_settings()
        
        # Set default retrieval parameters
        search_kwargs = kwargs.pop("search_kwargs", {})
        if "k" not in search_kwargs:
            search_kwargs["k"] = settings.retrieval_k
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs, **kwargs)
