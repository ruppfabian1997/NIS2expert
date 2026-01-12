# NIS2expert

A modular Python system for NIS-2 compliance management using LangChain.

## Overview

NIS2expert is a comprehensive compliance system that leverages LangChain and AI to help organizations understand, implement, and maintain compliance with the NIS-2 (Network and Information Security) Directive and ENISA guidelines.

## Features

### Core Retrieval Architecture
- **Document Loaders**: Support for PDF, DOCX, HTML, and text documents
- **Text Splitters**: Intelligent document chunking optimized for regulatory texts
- **Embeddings**: OpenAI embeddings for semantic search
- **Vector Stores**: Chroma and FAISS support for efficient document retrieval
- **LangChain Chains**: Pre-configured chains for Q&A and compliance checking

### Extensible Modules (Planned)
- **Auditing**: Compliance audit tracking and management
- **Gap Analysis**: Automated compliance gap identification
- **Scoring**: Compliance maturity and risk scoring
- **Reporting**: Automated compliance report generation

## Installation

### Requirements
- Python 3.9 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ruppfabian1997/NIS2expert.git
cd NIS2expert
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

3. Configure environment variables:

Create a `.env` file in the project root:
```env
NIS2_OPENAI_API_KEY=your-openai-api-key-here
```

## Project Structure

```
nis2expert/
├── __init__.py              # Package initialization
├── config.py                # Configuration management
├── loaders/                 # Document loaders
│   └── __init__.py
├── splitters/               # Text splitters
│   └── __init__.py
├── embeddings/              # Embeddings management
│   └── __init__.py
├── vectorstore/             # Vector store management
│   └── __init__.py
├── chains/                  # LangChain chains
│   └── __init__.py
├── auditing/                # Audit functionality (planned)
│   └── __init__.py
├── gap_analysis/            # Gap analysis (planned)
│   └── __init__.py
├── scoring/                 # Compliance scoring (planned)
│   └── __init__.py
├── reporting/               # Report generation (planned)
│   └── __init__.py
└── utils/                   # Utility functions
    └── __init__.py
```

## Quick Start

### Basic Usage

```python
from nis2expert.config import get_settings
from nis2expert.loaders import NIS2DocumentLoader
from nis2expert.splitters import NIS2TextSplitter
from nis2expert.embeddings import get_embeddings
from nis2expert.vectorstore import NIS2VectorStore
from nis2expert.chains import NIS2QAChain

# Load settings
settings = get_settings()

# Load documents
loader = NIS2DocumentLoader()
documents = loader.load_directory()

# Split documents
splitter = NIS2TextSplitter()
chunks = splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = get_embeddings()
vectorstore = NIS2VectorStore()
vectorstore.create_vectorstore(chunks, embeddings)

# Create QA chain
retriever = vectorstore.as_retriever()
qa_chain = NIS2QAChain(retriever=retriever)

# Ask questions
result = qa_chain.run("What are the main requirements of NIS-2?")
print(result['result'])
```

### Run Example

```bash
python examples/basic_usage.py
```

## Configuration

All configuration can be managed via environment variables with the `NIS2_` prefix or a `.env` file.

### Available Settings

| Setting | Environment Variable | Default | Description |
|---------|---------------------|---------|-------------|
| OpenAI API Key | `NIS2_OPENAI_API_KEY` | None | Required for embeddings and LLM |
| Data Directory | `NIS2_DATA_DIR` | `data` | Base directory for data |
| Documents Directory | `NIS2_DOCUMENTS_DIR` | `data/documents` | NIS-2 documents location |
| Vector Store Directory | `NIS2_VECTORSTORE_DIR` | `data/vectorstore` | Vector store persistence |
| Embedding Model | `NIS2_EMBEDDING_MODEL` | `text-embedding-ada-002` | OpenAI embedding model |
| Chunk Size | `NIS2_CHUNK_SIZE` | `1000` | Text chunk size |
| Chunk Overlap | `NIS2_CHUNK_OVERLAP` | `200` | Overlap between chunks |
| Vector Store Type | `NIS2_VECTORSTORE_TYPE` | `chroma` | Vector store type (chroma/faiss) |
| LLM Model | `NIS2_LLM_MODEL` | `gpt-3.5-turbo` | OpenAI chat model |
| LLM Temperature | `NIS2_LLM_TEMPERATURE` | `0.0` | Response temperature |
| Retrieval K | `NIS2_RETRIEVAL_K` | `4` | Number of documents to retrieve |

## Architecture

### Component Overview

1. **Loaders**: Load NIS-2 and ENISA documents from various formats
2. **Splitters**: Split documents into semantically meaningful chunks
3. **Embeddings**: Generate vector embeddings for semantic search
4. **Vector Store**: Store and retrieve document embeddings
5. **Chains**: LangChain chains for Q&A, compliance checking, and analysis

### Design Principles

- **Modularity**: Clear separation of concerns with independent components
- **Extensibility**: Easy to add new features and capabilities
- **Configuration**: Centralized configuration via environment variables
- **Type Safety**: Pydantic models for configuration validation
- **Logging**: Comprehensive logging for debugging and monitoring

## Use Cases

### Question Answering
Ask questions about NIS-2 requirements and get AI-powered answers with source citations.

### Compliance Checking
Compare organizational practices against NIS-2 requirements to identify compliance status.

### Document Analysis
Summarize and analyze NIS-2 documents and regulatory texts.

### Future Capabilities
- Gap analysis and remediation tracking
- Compliance maturity scoring
- Risk assessment
- Automated audit reporting

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License

## Support

For questions or issues, please open an issue on GitHub.
