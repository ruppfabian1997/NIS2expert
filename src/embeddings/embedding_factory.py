"""
Embedding factory for creating embedding models.
Supports OpenAI and HuggingFace embeddings with easy switching.
"""

import os
from typing import Optional
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings


def get_embeddings(
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> Embeddings:
    """
    Create an embedding model based on provider.
    
    This factory function allows easy switching between different
    embedding providers through configuration.
    
    Args:
        provider: Embedding provider ("openai" or "huggingface")
        model: Model name/identifier (provider-specific)
        **kwargs: Additional provider-specific arguments
        
    Returns:
        Embeddings instance
        
    Raises:
        ValueError: If provider is not supported
        
    Environment Variables:
        OPENAI_API_KEY: Required for OpenAI embeddings
        HF_TOKEN: Optional for HuggingFace private models
    """
    provider = provider.lower()
    
    if provider == "openai":
        return _get_openai_embeddings(model, **kwargs)
    elif provider == "huggingface":
        return _get_huggingface_embeddings(model, **kwargs)
    else:
        raise ValueError(
            f"Unsupported embedding provider: {provider}. "
            f"Supported providers: openai, huggingface"
        )


def _get_openai_embeddings(model: Optional[str] = None, **kwargs) -> OpenAIEmbeddings:
    """
    Create OpenAI embeddings.
    
    Args:
        model: OpenAI embedding model name
        **kwargs: Additional arguments for OpenAIEmbeddings
        
    Returns:
        OpenAIEmbeddings instance
    """
    if model is None:
        model = "text-embedding-ada-002"
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set in environment variables")
    
    return OpenAIEmbeddings(
        model=model,
        **kwargs
    )


def _get_huggingface_embeddings(
    model: Optional[str] = None,
    **kwargs
) -> HuggingFaceEmbeddings:
    """
    Create HuggingFace embeddings.
    
    Args:
        model: HuggingFace model identifier
        **kwargs: Additional arguments for HuggingFaceEmbeddings
        
    Returns:
        HuggingFaceEmbeddings instance
    """
    if model is None:
        # Default to a lightweight, effective model
        model = "sentence-transformers/all-MiniLM-L6-v2"
    
    return HuggingFaceEmbeddings(
        model_name=model,
        **kwargs
    )


# TODO: Add support for additional embedding providers
# - get_cohere_embeddings(): Cohere embeddings
# - get_vertex_ai_embeddings(): Google Vertex AI embeddings
# - get_azure_openai_embeddings(): Azure OpenAI embeddings

# TODO: NIS-2 specific embedding enhancements
# - fine_tuned_nis2_embeddings(): Custom fine-tuned model for compliance
# - multi_lingual_embeddings(): Support for EU languages
# - domain_adapted_embeddings(): Embeddings adapted for legal/regulatory text
