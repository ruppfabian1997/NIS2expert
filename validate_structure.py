#!/usr/bin/env python3
"""
Validate NIS2expert project structure without requiring dependencies.

This script checks:
- All Python files have valid syntax
- All expected files and directories exist
- Project structure matches specification
"""

import ast
import sys
from pathlib import Path


def validate_python_syntax(file_path: Path) -> bool:
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {file_path}: {e}")
        return False


def main():
    """Run validation checks."""
    project_root = Path(__file__).parent
    errors = []
    
    print("="*60)
    print("NIS2expert Project Structure Validation")
    print("="*60)
    
    # Check essential files
    print("\n1. Checking essential files...")
    essential_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        ".gitignore",
        ".env.example",
    ]
    
    for file in essential_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            errors.append(f"Missing file: {file}")
    
    # Check package structure
    print("\n2. Checking package structure...")
    package_root = project_root / "nis2expert"
    
    if package_root.exists():
        print(f"  ✓ nis2expert package directory exists")
    else:
        print(f"  ✗ nis2expert package directory missing")
        errors.append("Missing package directory")
        return 1
    
    # Check modules
    print("\n3. Checking modules...")
    modules = [
        "loaders",
        "splitters",
        "embeddings",
        "vectorstore",
        "chains",
        "auditing",
        "gap_analysis",
        "scoring",
        "reporting",
        "utils",
    ]
    
    for module in modules:
        module_path = package_root / module
        module_init = module_path / "__init__.py"
        
        if module_path.exists() and module_path.is_dir():
            if module_init.exists():
                print(f"  ✓ {module}/ with __init__.py")
            else:
                print(f"  ✗ {module}/ missing __init__.py")
                errors.append(f"Missing {module}/__init__.py")
        else:
            print(f"  ✗ {module}/ directory missing")
            errors.append(f"Missing {module}/ directory")
    
    # Check core Python files
    print("\n4. Checking core Python files...")
    core_files = [
        "nis2expert/__init__.py",
        "nis2expert/config.py",
    ]
    
    for file in core_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            errors.append(f"Missing file: {file}")
    
    # Check documentation
    print("\n5. Checking documentation...")
    docs_files = [
        "docs/architecture.md",
    ]
    
    for file in docs_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            errors.append(f"Missing file: {file}")
    
    # Check examples
    print("\n6. Checking examples...")
    example_files = [
        "examples/basic_usage.py",
    ]
    
    for file in example_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            errors.append(f"Missing file: {file}")
    
    # Validate Python syntax
    print("\n7. Validating Python syntax...")
    python_files = list(project_root.rglob("*.py"))
    
    # Filter out .git and __pycache__
    python_files = [
        f for f in python_files 
        if ".git" not in str(f) and "__pycache__" not in str(f)
    ]
    
    syntax_errors = 0
    for py_file in python_files:
        if validate_python_syntax(py_file):
            print(f"  ✓ {py_file.relative_to(project_root)}")
        else:
            syntax_errors += 1
            errors.append(f"Syntax error in {py_file}")
    
    # Summary
    print("\n" + "="*60)
    if errors:
        print(f"✗ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        print("="*60)
        return 1
    else:
        print("✓ All validation checks passed!")
        print(f"✓ Validated {len(python_files)} Python files")
        print(f"✓ Validated {len(modules)} modules")
        print("="*60)
        return 0


if __name__ == "__main__":
    sys.exit(main())
