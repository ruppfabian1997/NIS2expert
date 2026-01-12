"""
Document loader for NIS-2 and ENISA documents.
Supports PDF, TXT, DOCX, and HTML formats.
"""

from pathlib import Path
from typing import List, Optional
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    Docx2txtLoader,
)
from langchain.schema import Document


class DocumentLoader:
    """
    Unified document loader for various file formats.
    
    This loader handles NIS-2 compliance documents, ENISA guidelines,
    and other related documentation in multiple formats.
    """
    
    def __init__(self, supported_formats: Optional[List[str]] = None):
        """
        Initialize document loader.
        
        Args:
            supported_formats: List of supported file extensions.
                             Defaults to ['pdf', 'txt', 'docx', 'html']
        """
        if supported_formats is None:
            supported_formats = ['pdf', 'txt', 'docx', 'html']
        
        self.supported_formats = supported_formats
        
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects (may contain multiple pages/chunks)
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower().lstrip('.')
        
        if extension not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )
        
        # Select appropriate loader based on file extension
        loader = self._get_loader(file_path, extension)
        documents = loader.load()
        
        # TODO: Add metadata enrichment for NIS-2 specific documents
        # - Document type (directive, guideline, framework, etc.)
        # - Publication date
        # - Authority (ENISA, EU, national authority)
        # - Relevant articles/sections
        
        return documents
    
    def load_directory(self, directory_path: str, recursive: bool = True) -> List[Document]:
        """
        Load all documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            recursive: Whether to search subdirectories
            
        Returns:
            List of all loaded Document objects
        """
        dir_path = Path(directory_path)
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Invalid directory path: {directory_path}")
        
        all_documents = []
        
        # Determine search pattern
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        # Load all supported files
        for ext in self.supported_formats:
            for file_path in dir_path.glob(f"{pattern}.{ext}"):
                try:
                    docs = self.load_document(str(file_path))
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"Warning: Failed to load {file_path}: {e}")
        
        return all_documents
    
    def _get_loader(self, file_path: str, extension: str):
        """
        Get appropriate loader for file extension.
        
        Args:
            file_path: Path to the file
            extension: File extension (without dot)
            
        Returns:
            LangChain document loader instance
        """
        loaders = {
            'pdf': PyPDFLoader,
            'txt': TextLoader,
            'html': UnstructuredHTMLLoader,
            'docx': Docx2txtLoader,
        }
        
        loader_class = loaders.get(extension)
        if loader_class is None:
            raise ValueError(f"No loader available for extension: {extension}")
        
        return loader_class(file_path)
    
    # TODO: Add methods for NIS-2 specific document processing
    # - extract_nis2_requirements(): Extract specific compliance requirements
    # - categorize_by_pillar(): Categorize by NIS-2 security pillars
    # - extract_article_references(): Extract references to specific articles
    # - validate_document_structure(): Ensure document follows expected format
