"""
Utility functions for the NIS-2 Expert System.
Includes logging setup, configuration validation, and helper functions.
"""

import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional


def setup_logging(
    level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format string
        log_file: Path to log file (if None, logs to console only)
        
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
    )
    
    logger = logging.getLogger("nis2expert")
    logger.setLevel(numeric_level)
    
    # Add file handler if log file specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
    
    return logger


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_keys = [
        "embeddings",
        "vectorstore",
        "document_processing",
        "retrieval",
        "paths",
    ]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate embeddings config
    if "provider" not in config["embeddings"]:
        raise ValueError("embeddings.provider is required")
    
    # Validate vectorstore config
    if "provider" not in config["vectorstore"]:
        raise ValueError("vectorstore.provider is required")
    
    # Validate paths exist or can be created
    for path_key, path_value in config.get("paths", {}).items():
        path = Path(path_value)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create path {path_key}: {path_value} - {e}")
    
    return True


def ensure_directories(paths_config: Dict[str, str]) -> None:
    """
    Ensure all required directories exist.
    
    Args:
        paths_config: Dictionary of path configurations
    """
    for path_name, path_value in paths_config.items():
        path = Path(path_value)
        path.mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    # Assumes this file is in src/utils/
    return Path(__file__).parent.parent.parent


def format_retrieval_response(response: Dict[str, Any]) -> str:
    """
    Format a retrieval chain response for display.
    
    Args:
        response: Response dictionary from retrieval chain
        
    Returns:
        Formatted string response
    """
    output = []
    
    # Add answer
    if "result" in response:
        output.append("Answer:")
        output.append(response["result"])
        output.append("")
    elif "answer" in response:
        output.append("Answer:")
        output.append(response["answer"])
        output.append("")
    
    # Add source documents if available
    if "source_documents" in response and response["source_documents"]:
        output.append("Sources:")
        for i, doc in enumerate(response["source_documents"], 1):
            source = doc.metadata.get("source", "Unknown")
            output.append(f"{i}. {source}")
            # Optionally add page number if available
            if "page" in doc.metadata:
                output[-1] += f" (Page {doc.metadata['page']})"
        output.append("")
    
    return "\n".join(output)


def check_api_keys() -> Dict[str, bool]:
    """
    Check which API keys are configured.
    
    Returns:
        Dictionary mapping provider names to availability status
    """
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "huggingface": bool(os.getenv("HF_TOKEN")),
        "pinecone": bool(os.getenv("PINECONE_API_KEY")),
    }


# TODO: Add NIS-2 specific utility functions
# - parse_nis2_article_reference(): Parse article references from text
# - calculate_compliance_score(): Calculate overall compliance score
# - generate_audit_id(): Generate unique audit identifiers
# - format_compliance_report(): Format compliance reports
# - validate_nis2_document(): Validate document is NIS-2 related
# - extract_requirements_list(): Extract list of requirements from document
