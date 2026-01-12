"""
Document loaders for NIS-2/ENISA documents.

This module provides loaders for various document formats (PDF, DOCX, HTML, etc.)
with specific optimizations for regulatory and compliance documents.
"""

from pathlib import Path
from typing import List, Optional, Union

from langchain.schema import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    PDFMinerLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
    TextLoader,
)


class NIS2DocumentLoader:
    """
    Unified document loader for NIS-2/ENISA documents.
    
    Supports multiple document formats and provides a consistent interface
    for loading compliance-related documents.
    """
    
    SUPPORTED_EXTENSIONS = {
        ".pdf": PDFMinerLoader,
        ".docx": Docx2txtLoader,
        ".html": UnstructuredHTMLLoader,
        ".txt": TextLoader,
    }
    
    def __init__(self, documents_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the document loader.
        
        Args:
            documents_dir: Directory containing documents to load
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.documents_dir = Path(documents_dir) if documents_dir else settings.documents_dir
        
    def load_document(self, file_path: Union[str, Path]) -> List[Document]:
        """
        Load a single document.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects
            
        Raises:
            ValueError: If file format is not supported
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {', '.join(self.SUPPORTED_EXTENSIONS.keys())}"
            )
        
        loader_class = self.SUPPORTED_EXTENSIONS[extension]
        loader = loader_class(str(file_path))
        
        return loader.load()
    
    def load_directory(
        self,
        directory: Optional[Union[str, Path]] = None,
        glob_pattern: str = "**/*",
        show_progress: bool = True,
    ) -> List[Document]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory: Directory to load from (defaults to documents_dir)
            glob_pattern: Glob pattern for file matching
            show_progress: Whether to show loading progress
            
        Returns:
            List of Document objects
        """
        load_dir = Path(directory) if directory else self.documents_dir
        documents = []
        
        for ext in self.SUPPORTED_EXTENSIONS:
            pattern = f"{glob_pattern}{ext}"
            try:
                loader = DirectoryLoader(
                    str(load_dir),
                    glob=pattern,
                    loader_cls=self.SUPPORTED_EXTENSIONS[ext],
                    show_progress=show_progress,
                )
                documents.extend(loader.load())
            except Exception as e:
                print(f"Warning: Error loading {ext} files: {e}")
                continue
        
        return documents
    
    def load_pdf(self, file_path: Union[str, Path]) -> List[Document]:
        """
        Load a PDF document.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Document objects
        """
        loader = PDFMinerLoader(str(file_path))
        return loader.load()
    
    def load_docx(self, file_path: Union[str, Path]) -> List[Document]:
        """
        Load a DOCX document.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            List of Document objects
        """
        loader = Docx2txtLoader(str(file_path))
        return loader.load()
