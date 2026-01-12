"""
Text splitting functionality for document chunking.
Configurable text splitter for optimal retrieval performance.
"""

from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def get_text_splitter(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
) -> RecursiveCharacterTextSplitter:
    """
    Create and configure a text splitter for document chunking.
    
    The RecursiveCharacterTextSplitter is used to split documents into
    smaller chunks while preserving semantic meaning and context.
    
    Args:
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of overlapping characters between chunks
        separators: List of separators to use for splitting (in order of preference)
        
    Returns:
        Configured RecursiveCharacterTextSplitter instance
    """
    if separators is None:
        # Default separators optimized for structured documents
        # This order preserves document structure (paragraphs, then sentences, then words)
        separators = [
            "\n\n",  # Double newline (paragraph breaks)
            "\n",    # Single newline
            " ",     # Spaces
            "",      # Characters (fallback)
        ]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len,
    )
    
    return text_splitter


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
) -> List[Document]:
    """
    Split a list of documents into smaller chunks.
    
    Args:
        documents: List of Document objects to split
        chunk_size: Maximum size of each chunk in characters
        chunk_overlap: Number of overlapping characters between chunks
        separators: List of separators to use for splitting
        
    Returns:
        List of split Document objects
    """
    text_splitter = get_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    
    split_docs = text_splitter.split_documents(documents)
    
    # TODO: Add NIS-2 specific chunk processing
    # - Preserve article/section references in metadata
    # - Tag chunks with compliance categories
    # - Maintain relationships between requirement chunks
    # - Add semantic markers for better retrieval
    
    return split_docs


# TODO: Future enhancements for NIS-2 specific splitting
# - create_semantic_chunks(): Split based on compliance topics
# - preserve_article_context(): Ensure article references stay intact
# - smart_overlap(): Intelligent overlap based on content type
# - hierarchical_splitting(): Multi-level splitting for complex documents
