# NIS2expert Architecture

## Overview

NIS2expert is built as a modular, extensible system for NIS-2 compliance management using LangChain and AI-powered document retrieval.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     NIS2expert System                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │   Document     │  │     Text       │  │   Embeddings   │ │
│  │    Loaders     │─▶│   Splitters    │─▶│   Generation   │ │
│  └────────────────┘  └────────────────┘  └────────────────┘ │
│         │                                         │          │
│         │                                         ▼          │
│         │                              ┌────────────────┐    │
│         │                              │ Vector Store   │    │
│         │                              │ (Chroma/FAISS) │    │
│         │                              └────────────────┘    │
│         │                                         │          │
│         ▼                                         ▼          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LangChain Chains                        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐    │   │
│  │  │ QA Chain │ │Compliance│ │Document Summary  │    │   │
│  │  │          │ │  Check   │ │     Chain        │    │   │
│  │  └──────────┘ └──────────┘ └──────────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
│         │                                                     │
│         ▼                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Extensibility Layer (Future)                  │   │
│  │  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐ │   │
│  │  │Auditing  │ │   Gap    │ │Scoring │ │Reporting │ │   │
│  │  │          │ │ Analysis │ │        │ │          │ │   │
│  │  └──────────┘ └──────────┘ └────────┘ └──────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Document Loaders (`nis2expert.loaders`)

**Purpose**: Load NIS-2 and ENISA compliance documents from various sources.

**Features**:
- Multi-format support (PDF, DOCX, HTML, TXT)
- Directory-based bulk loading
- Consistent Document object output
- Error handling and logging

**Key Classes**:
- `NIS2DocumentLoader`: Main loader class with unified interface

### 2. Text Splitters (`nis2expert.splitters`)

**Purpose**: Split documents into semantically meaningful chunks for embedding and retrieval.

**Features**:
- Recursive character splitting with configurable separators
- Article/section-aware splitting for regulatory documents
- Configurable chunk size and overlap
- Metadata preservation

**Key Classes**:
- `NIS2TextSplitter`: Standard recursive splitter optimized for regulatory texts
- `ArticleAwareSplitter`: Preserves article boundaries when possible

### 3. Embeddings (`nis2expert.embeddings`)

**Purpose**: Generate vector embeddings for semantic search and retrieval.

**Features**:
- OpenAI embeddings integration
- Configurable embedding models
- Batch processing support
- Query and document embedding methods

**Key Classes**:
- `NIS2Embeddings`: Embeddings manager with configuration support

### 4. Vector Store (`nis2expert.vectorstore`)

**Purpose**: Store and retrieve document embeddings for similarity search.

**Features**:
- Multiple vector store backends (Chroma, FAISS)
- Persistence support
- Similarity search with scores
- Retriever interface for chains

**Key Classes**:
- `NIS2VectorStore`: Unified vector store manager

### 5. Chains (`nis2expert.chains`)

**Purpose**: Pre-configured LangChain chains for compliance tasks.

**Features**:
- Question-answering with source citations
- Compliance checking against requirements
- Document summarization
- Customizable prompts

**Key Classes**:
- `NIS2QAChain`: Retrieval-augmented Q&A
- `ComplianceCheckChain`: Gap analysis and compliance assessment
- `DocumentSummaryChain`: Document and section summarization

### 6. Configuration (`nis2expert.config`)

**Purpose**: Centralized configuration management.

**Features**:
- Environment variable support
- `.env` file loading
- Type validation with Pydantic
- Sensible defaults

**Key Classes**:
- `Settings`: Pydantic settings model
- `get_settings()`: Cached settings getter

### 7. Utilities (`nis2expert.utils`)

**Purpose**: Common helper functions.

**Features**:
- Logging setup
- Directory management
- Metadata formatting

## Extensibility Modules (Planned)

### Auditing (`nis2expert.auditing`)
- Audit log management
- Compliance audit workflows
- Evidence tracking
- Audit report generation

### Gap Analysis (`nis2expert.gap_analysis`)
- Automated gap identification
- Gap prioritization
- Remediation tracking
- Gap analysis reports

### Scoring (`nis2expert.scoring`)
- Compliance maturity scoring
- Risk-based assessment
- Score trending
- Benchmarking

### Reporting (`nis2expert.reporting`)
- Multi-format report generation (PDF, HTML, Excel)
- Customizable templates
- Executive summaries
- Scheduled reporting

## Data Flow

### Document Ingestion Pipeline

1. **Load**: Documents loaded from filesystem
2. **Split**: Split into overlapping chunks
3. **Embed**: Generate vector embeddings
4. **Store**: Store in vector database
5. **Index**: Create searchable index

### Query Pipeline

1. **Query**: User submits question
2. **Embed**: Convert query to vector
3. **Search**: Find similar document chunks
4. **Retrieve**: Get top-k relevant chunks
5. **Generate**: LLM generates answer with context
6. **Return**: Answer with source citations

### Compliance Check Pipeline

1. **Input**: Topic and current practices
2. **Retrieve**: Get relevant NIS-2 requirements
3. **Compare**: LLM compares practices vs requirements
4. **Assess**: Generate compliance assessment
5. **Report**: Structured compliance status

## Configuration Flow

```
Environment Variables / .env File
           ↓
    Settings (Pydantic)
           ↓
    Component Configuration
           ↓
    Runtime Behavior
```

## Design Patterns

### Factory Pattern
- Used in embeddings and vector store creation
- Allows easy switching between implementations

### Singleton Pattern
- Settings cached via `@lru_cache()`
- Ensures consistent configuration

### Strategy Pattern
- Different splitters for different use cases
- Pluggable vector store backends

### Template Method Pattern
- Base chain classes with customizable prompts
- Extensible chain implementations

## Scalability Considerations

### Current Implementation
- Suitable for small to medium document sets (< 10,000 documents)
- In-memory vector stores with disk persistence
- Synchronous processing

### Future Enhancements
- Batch processing for large document sets
- Distributed vector stores (Pinecone, Weaviate)
- Async processing pipelines
- Caching layers
- Rate limiting and quota management

## Security Considerations

- API keys stored in environment variables
- No hardcoded credentials
- Vector stores persisted locally (can be encrypted)
- Configurable data directories for compliance
- Future: Access control and audit logging

## Testing Strategy

### Unit Tests
- Test individual components in isolation
- Mock external dependencies (OpenAI API)
- Test configuration validation

### Integration Tests
- Test component interactions
- Test full pipelines
- Use test documents and fixtures

### End-to-End Tests
- Test complete workflows
- Validate output quality
- Performance benchmarks

## Deployment Considerations

### Local Development
- Virtual environment
- `.env` file for configuration
- Local vector store persistence

### Production
- Containerization (Docker)
- Environment-based configuration
- Persistent volume for vector stores
- Monitoring and logging
- API rate limiting

## Future Architecture

### Planned Enhancements
1. **Web API**: REST/GraphQL API for remote access
2. **UI**: Web interface for non-technical users
3. **Multi-tenancy**: Support multiple organizations
4. **Workflow Engine**: Automated compliance workflows
5. **Integration**: Connect to security tools and platforms
6. **Real-time Updates**: Monitor regulatory changes
7. **Collaboration**: Multi-user audit and assessment features
