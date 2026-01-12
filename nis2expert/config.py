"""
Configuration management for NIS2expert.

This module handles all configuration settings using pydantic-settings,
allowing configuration via environment variables or .env files.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with support for environment variables.
    
    All settings can be overridden via environment variables with the prefix NIS2_.
    For example: NIS2_OPENAI_API_KEY=xxx
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="NIS2_",
        case_sensitive=False,
    )
    
    # API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key for embeddings and LLM"
    )
    
    # Paths
    data_dir: Path = Field(
        default=Path("data"),
        description="Base directory for data storage"
    )
    
    documents_dir: Path = Field(
        default=Path("data/documents"),
        description="Directory containing NIS-2/ENISA documents"
    )
    
    vectorstore_dir: Path = Field(
        default=Path("data/vectorstore"),
        description="Directory for vector store persistence"
    )
    
    # Embeddings Configuration
    embedding_model: str = Field(
        default="text-embedding-ada-002",
        description="OpenAI embedding model to use"
    )
    
    # Text Splitting Configuration
    chunk_size: int = Field(
        default=1000,
        description="Size of text chunks for splitting"
    )
    
    chunk_overlap: int = Field(
        default=200,
        description="Overlap between consecutive chunks"
    )
    
    # Vector Store Configuration
    vectorstore_type: str = Field(
        default="chroma",
        description="Type of vector store (chroma, faiss)"
    )
    
    collection_name: str = Field(
        default="nis2_documents",
        description="Collection name in vector store"
    )
    
    # Retrieval Configuration
    retrieval_k: int = Field(
        default=4,
        description="Number of documents to retrieve"
    )
    
    # LLM Configuration
    llm_model: str = Field(
        default="gpt-3.5-turbo",
        description="OpenAI model for chat/completion"
    )
    
    llm_temperature: float = Field(
        default=0.0,
        description="Temperature for LLM responses"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.documents_dir.mkdir(parents=True, exist_ok=True)
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    settings = Settings()
    settings.ensure_directories()
    return settings
