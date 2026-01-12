#!/usr/bin/env python3
"""
Validation script to verify the project structure.
This script checks that all files and directories are in place.
"""

import os
from pathlib import Path


def check_structure():
    """Check that all required files and directories exist."""
    
    base_path = Path(__file__).parent
    
    # Required directories
    required_dirs = [
        "src",
        "src/config",
        "src/loaders",
        "src/splitters",
        "src/embeddings",
        "src/vectorstore",
        "src/chains",
        "src/utils",
        "data",
        "data/documents",
        "data/vectorstore",
        "data/reports",
        "data/audit_logs",
        "logs",
    ]
    
    # Required files
    required_files = [
        "config.yaml",
        "main.py",
        "setup.py",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "README.md",
        "src/__init__.py",
        "src/config/__init__.py",
        "src/config/config_loader.py",
        "src/loaders/__init__.py",
        "src/loaders/document_loader.py",
        "src/splitters/__init__.py",
        "src/splitters/text_splitter.py",
        "src/embeddings/__init__.py",
        "src/embeddings/embedding_factory.py",
        "src/vectorstore/__init__.py",
        "src/vectorstore/vectorstore_factory.py",
        "src/chains/__init__.py",
        "src/chains/retrieval_chain.py",
        "src/utils/__init__.py",
        "src/utils/helpers.py",
    ]
    
    print("Checking project structure...\n")
    
    all_ok = True
    
    # Check directories
    print("Directories:")
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING")
            all_ok = False
    
    print("\nFiles:")
    # Check files
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists() and full_path.is_file():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_ok = False
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ Project structure is complete and correct!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up API keys: cp .env.example .env (and edit)")
        print("3. Add documents to data/documents/")
        print("4. Run the system: python main.py")
    else:
        print("❌ Some files or directories are missing!")
        return 1
    
    print("="*70)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(check_structure())
