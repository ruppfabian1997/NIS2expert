"""
Utility functions for NIS2expert.

This module provides common utility functions used across the package.
"""

import logging
from pathlib import Path
from typing import Optional


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Configured logger
    """
    from nis2expert.config import get_settings
    
    settings = get_settings()
    level = log_level or settings.log_level
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    
    return logging.getLogger('nis2expert')


def ensure_directory(path: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(file_path: Path) -> str:
    """
    Get the file extension in lowercase.
    
    Args:
        file_path: File path
        
    Returns:
        File extension (e.g., '.pdf')
    """
    return Path(file_path).suffix.lower()


def format_metadata(metadata: dict) -> dict:
    """
    Format document metadata for consistency.
    
    Args:
        metadata: Raw metadata dictionary
        
    Returns:
        Formatted metadata
    """
    formatted = {}
    
    # Convert Path objects to strings
    for key, value in metadata.items():
        if isinstance(value, Path):
            formatted[key] = str(value)
        else:
            formatted[key] = value
    
    return formatted
