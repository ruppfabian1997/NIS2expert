"""
Text splitters for NIS-2 documents.

This module provides text splitting functionality optimized for regulatory
and compliance documents, preserving context and structure.
"""

from typing import List, Optional

from langchain.schema import Document
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


class NIS2TextSplitter:
    """
    Text splitter optimized for NIS-2/ENISA compliance documents.
    
    Provides intelligent text splitting that preserves document structure
    and context for better retrieval performance.
    """
    
    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        separators: Optional[List[str]] = None,
    ):
        """
        Initialize the text splitter.
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            separators: Custom separators for splitting
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        # Default separators optimized for regulatory documents
        # Prioritize section/article breaks, then paragraphs, then sentences
        self.separators = separators or [
            "\n\n\n",  # Major section breaks
            "\n\n",    # Paragraph breaks
            "\n",      # Line breaks
            ". ",      # Sentence breaks
            ", ",      # Clause breaks
            " ",       # Word breaks
            "",        # Character breaks
        ]
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split a list of documents into chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        return self.splitter.split_documents(documents)
    
    def split_text(self, text: str) -> List[str]:
        """
        Split a text string into chunks.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        return self.splitter.split_text(text)
    
    def create_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[dict]] = None,
    ) -> List[Document]:
        """
        Create Document objects from texts with metadata.
        
        Args:
            texts: List of text strings
            metadatas: List of metadata dicts (one per text)
            
        Returns:
            List of Document objects
        """
        return self.splitter.create_documents(texts, metadatas=metadatas)


class ArticleAwareSplitter:
    """
    Splitter that attempts to preserve article/section boundaries in regulatory documents.
    
    This is useful for NIS-2 documents where articles and sections should remain intact
    when possible for better context preservation.
    """
    
    def __init__(
        self,
        max_chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ):
        """
        Initialize the article-aware splitter.
        
        Args:
            max_chunk_size: Maximum size of chunks
            chunk_overlap: Overlap between chunks
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.max_chunk_size = max_chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        # Splitter for articles/sections
        self.section_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=self.max_chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        # Fallback splitter for oversized sections
        self.fallback_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents while attempting to preserve article boundaries.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        chunks = []
        
        for doc in documents:
            # First try section-aware splitting
            section_chunks = self.section_splitter.split_documents([doc])
            
            # For any chunks that are too large, use fallback splitter
            for chunk in section_chunks:
                if len(chunk.page_content) > self.max_chunk_size:
                    chunks.extend(self.fallback_splitter.split_documents([chunk]))
                else:
                    chunks.append(chunk)
        
        return chunks
