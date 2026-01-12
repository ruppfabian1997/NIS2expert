"""
Configuration loader for NIS-2 Expert System.
Handles loading and validation of configuration from YAML file.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """Configuration class for NIS-2 Expert System."""
    
    def __init__(self, config_dict: Dict[str, Any]):
        """
        Initialize configuration from dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values
        """
        self._config = config_dict
        
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated key path.
        
        Args:
            key: Dot-separated key path (e.g., 'embeddings.provider')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
                
        return value
    
    def get_embeddings_config(self) -> Dict[str, Any]:
        """Get embeddings configuration."""
        return self._config.get('embeddings', {})
    
    def get_vectorstore_config(self) -> Dict[str, Any]:
        """Get vector store configuration."""
        return self._config.get('vectorstore', {})
    
    def get_retrieval_config(self) -> Dict[str, Any]:
        """Get retrieval chain configuration."""
        return self._config.get('retrieval', {})
    
    def get_document_processing_config(self) -> Dict[str, Any]:
        """Get document processing configuration."""
        return self._config.get('document_processing', {})
    
    def get_paths_config(self) -> Dict[str, Any]:
        """Get paths configuration."""
        return self._config.get('paths', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get('logging', {})


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file. If None, uses default config.yaml
        
    Returns:
        Config object
        
    Raises:
        FileNotFoundError: If configuration file not found
        yaml.YAMLError: If YAML parsing fails
    """
    if config_path is None:
        # Default to config.yaml in project root
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config.yaml"
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_dict = yaml.safe_load(f)
    
    # Load environment variable overrides
    _apply_env_overrides(config_dict)
    
    return Config(config_dict)


def _apply_env_overrides(config_dict: Dict[str, Any]) -> None:
    """
    Apply environment variable overrides to configuration.
    
    Environment variables should be prefixed with NIS2_ and use underscores
    for nested keys (e.g., NIS2_EMBEDDINGS_PROVIDER).
    
    Args:
        config_dict: Configuration dictionary to update
    """
    env_prefix = "NIS2_"
    
    for env_key, env_value in os.environ.items():
        if env_key.startswith(env_prefix):
            # Remove prefix and convert to lowercase
            key_path = env_key[len(env_prefix):].lower().split('_')
            
            # Navigate to the right place in config dict
            current = config_dict
            for key in key_path[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[key_path[-1]] = env_value
