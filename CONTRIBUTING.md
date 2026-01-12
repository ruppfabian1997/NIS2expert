# Contributing to NIS-2 Compliance Expert System

Thank you for your interest in contributing! This document provides guidelines and information for developers.

## Project Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Entry Point & Orchestration)            │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │ Config   │  │ Loaders  │  │ Splitters│
         └──────────┘  └──────────┘  └──────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │Embeddings│  │VectorStore│ │  Chains  │
         └──────────┘  └──────────┘  └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  Utils   │
                        └──────────┘
```

### Design Principles

1. **Modularity**: Each component is independent and replaceable
2. **Factory Pattern**: Used for creating instances (embeddings, vector stores, chains)
3. **Configuration-Driven**: Behavior controlled via `config.yaml`
4. **Extensibility**: Easy to add new providers without changing existing code
5. **Clean Separation**: Business logic separate from infrastructure

## Development Setup

### 1. Clone and Install

```bash
git clone https://github.com/ruppfabian1997/NIS2expert.git
cd NIS2expert
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Install Development Dependencies

```bash
pip install pytest pytest-cov black flake8 mypy
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Formatting

Use Black for code formatting:

```bash
black src/ main.py
```

### Linting

Run flake8 before committing:

```bash
flake8 src/ --max-line-length=100
```

### Type Checking

```bash
mypy src/
```

## Adding New Features

### Adding a New Embedding Provider

1. Add provider configuration to `config.yaml`
2. Create `_get_<provider>_embeddings()` in `src/embeddings/embedding_factory.py`
3. Add provider case to `get_embeddings()` function
4. Update documentation

Example:
```python
def _get_cohere_embeddings(model: Optional[str] = None, **kwargs):
    """Create Cohere embeddings."""
    # Implementation
    pass

# In get_embeddings():
elif provider == "cohere":
    return _get_cohere_embeddings(model, **kwargs)
```

### Adding a New Vector Store

1. Add provider configuration to `config.yaml`
2. Implement `_get_<provider>_vectorstore()` and `_create_<provider>_from_docs()`
3. Add provider case to factory functions
4. Update documentation

### Adding a New Chain Type

1. Add chain configuration to `config.yaml`
2. Implement chain creation function in `src/chains/retrieval_chain.py`
3. Add chain type case to `get_retrieval_chain()`
4. Document usage

### Adding NIS-2 Specific Features

Many TODOs in the code mark extension points for NIS-2 features:

#### Gap Analysis
Location: `src/chains/retrieval_chain.py`
```python
# TODO: create_gap_analysis_chain()
```

#### Compliance Scoring
Location: `src/utils/helpers.py`
```python
# TODO: calculate_compliance_score()
```

#### Audit Trail
Location: Throughout, especially in chains and main.py

## Testing

### Writing Tests

Create tests in a `tests/` directory:

```
tests/
├── test_config.py
├── test_loaders.py
├── test_splitters.py
├── test_embeddings.py
├── test_vectorstore.py
├── test_chains.py
└── test_utils.py
```

### Test Structure

```python
import pytest
from src.config import load_config

def test_load_config():
    """Test configuration loading."""
    config = load_config()
    assert config is not None
    assert config.get("embeddings.provider") in ["openai", "huggingface"]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_config.py
```

## Project Structure Guidelines

### When to Create a New Module

Create a new module when:
- Functionality is distinct and self-contained
- It has clear inputs and outputs
- It might be reused in multiple places
- It implements a specific design pattern

### When to Extend Existing Module

Extend existing modules when:
- Adding a new provider/implementation
- Enhancing existing functionality
- Adding helper functions for existing features

## Documentation

### Code Documentation

- All public functions must have docstrings
- Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
    """
    pass
```

### README Updates

When adding features:
1. Update main README.md with usage examples
2. Update QUICKSTART.md if it affects setup
3. Update this CONTRIBUTING.md if it affects development

## Pull Request Process

### Before Submitting

1. ✅ Run tests: `pytest`
2. ✅ Format code: `black .`
3. ✅ Lint code: `flake8 src/`
4. ✅ Update documentation
5. ✅ Add/update tests for new features

### PR Description

Include:
- What problem does this solve?
- What changes were made?
- How to test the changes?
- Any breaking changes?

### Example PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test the changes

## Checklist
- [ ] Tests pass
- [ ] Code formatted with Black
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Commit Messages

Use clear, descriptive commit messages:

```
Add Pinecone vector store implementation

- Implement _get_pinecone_vectorstore()
- Implement _create_pinecone_from_docs()
- Add Pinecone configuration to config.yaml
- Update README with Pinecone setup instructions
```

## Future Roadmap

Priority features to implement:

1. **Gap Analysis Chain** - Identify compliance gaps
2. **Compliance Scoring** - Automated scoring system
3. **Report Generation** - PDF/HTML compliance reports
4. **Audit Trail** - Complete logging of all interactions
5. **Multi-language Support** - Support all EU languages
6. **Fine-tuned Models** - Domain-specific embeddings
7. **Web Interface** - Flask/FastAPI web UI
8. **Additional Vector Stores** - Pinecone, Weaviate, Chroma
9. **Batch Processing** - Process multiple queries efficiently
10. **Integration APIs** - REST API for external systems

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Tag issues appropriately (bug, enhancement, question)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
