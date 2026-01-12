"""
NIS2expert - NIS-2 Compliance System with LangChain

A modular Python package for intelligent NIS-2 and ENISA document retrieval,
analysis, and compliance management.
"""

__version__ = "0.1.0"

from nis2expert.config import Settings, get_settings

__all__ = ["Settings", "get_settings", "__version__"]
