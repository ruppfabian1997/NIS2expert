# NIS-2 Compliance Expert System

A modular LangChain-based system for NIS-2 compliance auditing, gap analysis, and expert consultation.

## Overview

This project provides a clean, extensible framework for building a NIS-2 compliance expert system using LangChain. It implements a retrieval-augmented generation (RAG) architecture to answer questions about NIS-2 directive requirements, ENISA guidelines, and compliance best practices.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for each component
- **Multiple Embedding Providers**: Support for OpenAI and HuggingFace embeddings (easily switchable via config)
- **Flexible Vector Stores**: FAISS (local) implemented, with abstraction layer for Pinecone, Weaviate, and Chroma
- **Document Processing**: Support for PDF, TXT, DOCX, and HTML formats
- **Configurable Retrieval**: RetrievalQA and ConversationalRetrievalChain options
- **Extensible Design**: Prepared for future features like gap analysis, compliance scoring, and automated reporting

## Project Structure

```
NIS2expert/
├── src/
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── config_loader.py
│   ├── loaders/             # Document loaders
│   │   ├── __init__.py
│   │   └── document_loader.py
│   ├── splitters/           # Text splitting/chunking
│   │   ├── __init__.py
│   │   └── text_splitter.py
│   ├── embeddings/          # Embedding models
│   │   ├── __init__.py
│   │   └── embedding_factory.py
│   ├── vectorstore/         # Vector database implementations
│   │   ├── __init__.py
│   │   └── vectorstore_factory.py
│   ├── chains/              # LangChain retrieval chains
│   │   ├── __init__.py
│   │   └── retrieval_chain.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── data/
│   ├── documents/           # Place your NIS-2 documents here
│   ├── vectorstore/         # Vector indices stored here
│   ├── reports/             # Generated reports (future)
│   └── audit_logs/          # Audit trails (future)
├── logs/                    # Application logs
├── config.yaml              # Main configuration file
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # This file
```

## Requirements

- Python 3.10 or higher
- LangChain and related dependencies
- API keys for chosen providers (OpenAI, HuggingFace, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ruppfabian1997/NIS2expert.git
cd NIS2expert
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API keys:
```bash
# For OpenAI (default)
export OPENAI_API_KEY='your-openai-api-key'

# For HuggingFace (optional, for private models)
export HF_TOKEN='your-huggingface-token'
```

## Configuration

Edit `config.yaml` to customize the system:

- **Embeddings Provider**: Choose between `openai` or `huggingface`
- **Vector Store**: Currently supports `faiss` (local), prepared for `pinecone`, `weaviate`, `chroma`
- **Document Processing**: Configure chunk size, overlap, and supported formats
- **Retrieval Settings**: Adjust number of documents retrieved, LLM model, temperature, etc.

Example configuration snippet:
```yaml
embeddings:
  provider: "openai"  # or "huggingface"
  
vectorstore:
  provider: "faiss"
  faiss:
    index_path: "data/vectorstore/faiss_index"
    
retrieval:
  chain_type: "retrieval_qa"
  search_kwargs:
    k: 4  # Number of documents to retrieve
```

## Usage

### 1. Add NIS-2 Documents

Place your NIS-2 directive PDFs, ENISA guidelines, and related documents in the `data/documents/` directory.

### 2. Run the System

```bash
python main.py
```

The system will:
1. Load configuration
2. Initialize embeddings and vector store
3. Process and index your documents (first run)
4. Start an interactive Q&A session

### 3. Ask Questions

```
Question: What are the main security requirements under NIS-2?
Question: Which organizations are covered by the NIS-2 directive?
Question: What are the reporting obligations for security incidents?
```

## Customization

### Using HuggingFace Embeddings

Edit `config.yaml`:
```yaml
embeddings:
  provider: "huggingface"
  huggingface:
    model_name: "sentence-transformers/all-MiniLM-L6-v2"
```

### Changing Chunk Size

Edit `config.yaml`:
```yaml
document_processing:
  splitter:
    chunk_size: 1500
    chunk_overlap: 300
```

### Using Conversational Chain

Edit `config.yaml`:
```yaml
retrieval:
  chain_type: "conversational_retrieval"
```

## Future Enhancements

The codebase includes TODOs and placeholders for:

- **Gap Analysis**: Identify compliance gaps in your organization
- **Compliance Scoring**: Automated scoring of compliance levels
- **Audit Trail**: Track all queries and responses for audit purposes
- **Report Generation**: Automated compliance reports
- **Multi-language Support**: Support for all EU languages
- **Fine-tuned Models**: Domain-specific embeddings for regulatory text
- **Additional Vector Stores**: Pinecone, Weaviate, Chroma integration

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests (when implemented)
pytest
```

### Code Quality

```bash
# Format code
pip install black
black .

# Lint code
pip install flake8
flake8 src/

# Type checking
pip install mypy
mypy src/
```

## Architecture Notes

### Component Separation

Each module is designed to be independent and replaceable:

- **Loaders**: Handle different document formats
- **Splitters**: Manage text chunking strategies
- **Embeddings**: Abstract embedding model selection
- **VectorStore**: Provide database-agnostic interface
- **Chains**: Implement retrieval and response logic
- **Utils**: Offer supporting functionality

### Extensibility

The factory pattern is used throughout to make it easy to add new providers:

```python
# Adding a new embedding provider
def _get_cohere_embeddings(model, **kwargs):
    # Implementation here
    pass

# Register in get_embeddings()
elif provider == "cohere":
    return _get_cohere_embeddings(model, **kwargs)
```

## Troubleshooting

### API Key Issues

If you see API key errors:
1. Verify your environment variables are set
2. Try using HuggingFace embeddings (no API key required for public models)
3. Check API key validity and quotas

### Memory Issues

If processing large documents:
1. Reduce `chunk_size` in config
2. Process documents in batches
3. Use FAISS with smaller indices

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

Built with:
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [HuggingFace](https://huggingface.co/)
- [FAISS](https://github.com/facebookresearch/faiss)
