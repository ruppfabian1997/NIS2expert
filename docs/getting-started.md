# Getting Started with NIS2expert

This guide will help you set up and start using NIS2expert for NIS-2 compliance management.

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (for embeddings and LLM functionality)
- NIS-2 or ENISA documents (PDF, DOCX, HTML, or TXT format)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ruppfabian1997/NIS2expert.git
cd NIS2expert
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or for development:

```bash
pip install -e ".[dev]"
```

### 4. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
NIS2_OPENAI_API_KEY=your-api-key-here
```

## Quick Start

### Step 1: Add Documents

Place your NIS-2 and ENISA documents in the `data/documents/` directory:

```bash
mkdir -p data/documents
# Copy your PDF, DOCX, or other documents to data/documents/
```

### Step 2: Run the Example

```bash
python examples/basic_usage.py
```

This will:
1. Load documents from `data/documents/`
2. Split them into chunks
3. Create embeddings
4. Build a vector store
5. Run example queries

## Usage Examples

### Basic Document Loading

```python
from nis2expert.loaders import NIS2DocumentLoader

# Load all documents from a directory
loader = NIS2DocumentLoader()
documents = loader.load_directory()

# Load a specific PDF
documents = loader.load_pdf("path/to/document.pdf")
```

### Text Splitting

```python
from nis2expert.splitters import NIS2TextSplitter

# Create a splitter with default settings
splitter = NIS2TextSplitter()

# Split documents into chunks
chunks = splitter.split_documents(documents)

# Use article-aware splitter for regulatory documents
from nis2expert.splitters import ArticleAwareSplitter

article_splitter = ArticleAwareSplitter()
chunks = article_splitter.split_documents(documents)
```

### Creating Embeddings and Vector Store

```python
from nis2expert.embeddings import get_embeddings
from nis2expert.vectorstore import NIS2VectorStore

# Create embeddings
embeddings = get_embeddings()

# Create vector store
vectorstore = NIS2VectorStore()
vectorstore.create_vectorstore(chunks, embeddings)

# Later, load existing vector store
vectorstore = NIS2VectorStore()
vectorstore.load_vectorstore(embeddings)
```

### Question Answering

```python
from nis2expert.chains import NIS2QAChain

# Create a retriever from vector store
retriever = vectorstore.as_retriever()

# Create QA chain
qa_chain = NIS2QAChain(retriever=retriever)

# Ask questions
result = qa_chain.run("What are the reporting obligations under NIS-2?")
print(result['result'])
print(f"Sources: {len(result['source_documents'])}")
```

### Compliance Checking

```python
from nis2expert.chains import ComplianceCheckChain

# Create compliance check chain
compliance_chain = ComplianceCheckChain(retriever=retriever)

# Define current practices
current_practices = """
Our organization has:
- Annual security training
- Incident response plan
- Vulnerability scanning
"""

# Check compliance
assessment = compliance_chain.check_compliance(
    topic="security measures and incident response",
    current_practices=current_practices
)
print(assessment)
```

### Document Summarization

```python
from nis2expert.chains import DocumentSummaryChain

# Create summary chain
summary_chain = DocumentSummaryChain()

# Summarize documents
summary = summary_chain.summarize_documents(documents)
print(summary)
```

## Configuration

### Environment Variables

All settings can be configured via environment variables:

```bash
# Required
export NIS2_OPENAI_API_KEY=your-key

# Optional - Data Paths
export NIS2_DATA_DIR=data
export NIS2_DOCUMENTS_DIR=data/documents
export NIS2_VECTORSTORE_DIR=data/vectorstore

# Optional - Model Configuration
export NIS2_EMBEDDING_MODEL=text-embedding-ada-002
export NIS2_LLM_MODEL=gpt-3.5-turbo
export NIS2_LLM_TEMPERATURE=0.0

# Optional - Text Splitting
export NIS2_CHUNK_SIZE=1000
export NIS2_CHUNK_OVERLAP=200

# Optional - Vector Store
export NIS2_VECTORSTORE_TYPE=chroma  # or 'faiss'
export NIS2_COLLECTION_NAME=nis2_documents

# Optional - Retrieval
export NIS2_RETRIEVAL_K=4

# Optional - Logging
export NIS2_LOG_LEVEL=INFO
```

### Programmatic Configuration

```python
from nis2expert.config import get_settings

# Get current settings
settings = get_settings()

# Access settings
print(settings.chunk_size)
print(settings.embedding_model)
```

## Project Structure

```
NIS2expert/
├── data/                       # Data directory (created automatically)
│   ├── documents/              # Place your NIS-2 docs here
│   └── vectorstore/            # Vector store persistence
├── docs/                       # Documentation
│   └── architecture.md         # Architecture documentation
├── examples/                   # Example scripts
│   └── basic_usage.py          # Basic usage example
├── nis2expert/                 # Main package
│   ├── __init__.py
│   ├── config.py               # Configuration
│   ├── loaders/                # Document loaders
│   ├── splitters/              # Text splitters
│   ├── embeddings/             # Embeddings management
│   ├── vectorstore/            # Vector store
│   ├── chains/                 # LangChain chains
│   ├── auditing/               # Audit features (planned)
│   ├── gap_analysis/           # Gap analysis (planned)
│   ├── scoring/                # Scoring (planned)
│   ├── reporting/              # Reporting (planned)
│   └── utils/                  # Utilities
├── tests/                      # Tests
├── .env.example                # Example environment file
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # Project metadata
├── README.md                   # Main README
└── requirements.txt            # Dependencies
```

## Common Tasks

### Update Documents

1. Add new documents to `data/documents/`
2. Re-run document loading and vector store creation:

```python
from nis2expert.loaders import NIS2DocumentLoader
from nis2expert.splitters import NIS2TextSplitter
from nis2expert.embeddings import get_embeddings
from nis2expert.vectorstore import NIS2VectorStore

# Load new documents
loader = NIS2DocumentLoader()
documents = loader.load_directory()

# Split and create embeddings
splitter = NIS2TextSplitter()
chunks = splitter.split_documents(documents)

embeddings = get_embeddings()

# Recreate vector store
vectorstore = NIS2VectorStore()
vectorstore.create_vectorstore(chunks, embeddings)
```

### Switch Vector Store

Edit `.env` to change vector store type:

```bash
# Use FAISS instead of Chroma
NIS2_VECTORSTORE_TYPE=faiss
```

### Customize Prompts

```python
from nis2expert.chains import NIS2QAChain

custom_prompt = """You are an expert on NIS-2 compliance.
Context: {context}
Question: {question}
Detailed Answer:"""

qa_chain = NIS2QAChain(
    retriever=retriever,
    prompt_template=custom_prompt
)
```

## Troubleshooting

### API Key Issues

If you get "OpenAI API key not found" errors:

1. Check `.env` file exists and contains `NIS2_OPENAI_API_KEY=your-key`
2. Ensure the `.env` file is in the project root
3. Restart your Python session after adding the key

### Import Errors

If you get module import errors:

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# If using development mode
pip install -e .
```

### Vector Store Errors

If you get vector store errors:

1. Delete the `data/vectorstore/` directory
2. Recreate the vector store from scratch
3. Ensure you have write permissions in the data directory

## Next Steps

- Read the [Architecture Documentation](docs/architecture.md) to understand the system design
- Explore the example scripts in `examples/`
- Add your own NIS-2 documents for analysis
- Customize chains and prompts for your specific needs
- Contribute to the project!

## Getting Help

- Open an issue on GitHub
- Check the documentation in `docs/`
- Review the example scripts in `examples/`
