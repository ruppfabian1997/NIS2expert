"""
Main entry point for NIS-2 Compliance Expert System.

This script demonstrates the basic usage of the system:
1. Load configuration
2. Initialize components
3. Load and process documents
4. Create vector store
5. Run queries
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import load_config
from src.loaders import DocumentLoader
from src.splitters import get_text_splitter, split_documents
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore_from_docs, get_vectorstore
from src.chains import get_retrieval_chain
from src.utils import setup_logging, validate_config, ensure_directories, format_retrieval_response


def main():
    """Main execution function."""
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Validate configuration
    validate_config(config._config)
    
    # Setup logging
    logging_config = config.get_logging_config()
    logger = setup_logging(
        level=logging_config.get("level", "INFO"),
        log_format=logging_config.get("format"),
        log_file=logging_config.get("file")
    )
    
    logger.info("NIS-2 Compliance Expert System starting...")
    
    # Ensure required directories exist
    paths_config = config.get_paths_config()
    ensure_directories(paths_config)
    logger.info("Directory structure verified")
    
    # Initialize components based on configuration
    embeddings_config = config.get_embeddings_config()
    embeddings_provider = embeddings_config.get("provider", "openai")
    
    logger.info(f"Initializing embeddings provider: {embeddings_provider}")
    
    # Get provider-specific config
    if embeddings_provider == "openai":
        model = embeddings_config.get("openai", {}).get("model")
    elif embeddings_provider == "huggingface":
        model = embeddings_config.get("huggingface", {}).get("model_name")
    else:
        model = None
    
    try:
        embeddings = get_embeddings(provider=embeddings_provider, model=model)
        logger.info("Embeddings initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize embeddings: {e}")
        print(f"Error: {e}")
        print("\nPlease ensure you have set the required API keys:")
        print("  - For OpenAI: export OPENAI_API_KEY='your-key'")
        print("  - For HuggingFace (optional): export HF_TOKEN='your-token'")
        return 1
    
    # Example workflow: Load documents, create vector store, and query
    print("\n" + "="*70)
    print("NIS-2 Compliance Expert System - Example Workflow")
    print("="*70)
    
    # Check if documents exist
    documents_path = Path(paths_config.get("documents", "data/documents"))
    
    if not documents_path.exists() or not any(documents_path.iterdir()):
        print(f"\nNo documents found in {documents_path}")
        print("To use the system:")
        print(f"  1. Place NIS-2 and ENISA documents in {documents_path}")
        print("  2. Run this script again to index the documents")
        print("\nExample usage after adding documents:")
        print("  python main.py")
        
        # Create example directory structure
        documents_path.mkdir(parents=True, exist_ok=True)
        print(f"\nCreated directory: {documents_path}")
        print("Add your PDF, TXT, DOCX, or HTML documents there.")
        
        return 0
    
    # Load documents
    print(f"\nLoading documents from {documents_path}...")
    doc_processing_config = config.get_document_processing_config()
    loader = DocumentLoader(
        supported_formats=doc_processing_config.get("supported_formats")
    )
    
    try:
        documents = loader.load_directory(str(documents_path))
        print(f"Loaded {len(documents)} document chunks")
        logger.info(f"Loaded {len(documents)} documents from {documents_path}")
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        print(f"Error loading documents: {e}")
        return 1
    
    # Split documents
    print("Splitting documents into chunks...")
    splitter_config = doc_processing_config.get("splitter", {})
    split_docs = split_documents(
        documents,
        chunk_size=splitter_config.get("chunk_size", 1000),
        chunk_overlap=splitter_config.get("chunk_overlap", 200),
        separators=splitter_config.get("separators")
    )
    print(f"Created {len(split_docs)} text chunks")
    logger.info(f"Split into {len(split_docs)} chunks")
    
    # Create or load vector store
    vectorstore_config = config.get_vectorstore_config()
    vectorstore_provider = vectorstore_config.get("provider", "faiss")
    
    print(f"\nInitializing {vectorstore_provider} vector store...")
    
    if vectorstore_provider == "faiss":
        index_path = vectorstore_config.get("faiss", {}).get("index_path", "data/vectorstore/faiss_index")
        index_path_obj = Path(index_path)
        
        # Check if index already exists
        if index_path_obj.exists():
            print(f"Loading existing index from {index_path}")
            try:
                vectorstore = get_vectorstore(
                    provider=vectorstore_provider,
                    embeddings=embeddings,
                    index_path=index_path
                )
                logger.info("Loaded existing vector store")
            except Exception as e:
                logger.warning(f"Failed to load existing index: {e}")
                print(f"Creating new index...")
                vectorstore = create_vectorstore_from_docs(
                    split_docs,
                    embeddings,
                    provider=vectorstore_provider,
                    index_path=index_path
                )
                logger.info("Created new vector store")
        else:
            print(f"Creating new index at {index_path}")
            vectorstore = create_vectorstore_from_docs(
                split_docs,
                embeddings,
                provider=vectorstore_provider,
                index_path=index_path
            )
            logger.info("Created new vector store")
    else:
        print(f"Provider {vectorstore_provider} not yet fully implemented")
        return 1
    
    print("Vector store ready!")
    
    # Create retrieval chain
    print("\nInitializing retrieval chain...")
    retrieval_config = config.get_retrieval_config()
    chain_type = retrieval_config.get("chain_type", "retrieval_qa")
    
    chain = get_retrieval_chain(
        vectorstore=vectorstore,
        chain_type=chain_type,
        # LLM will be created with defaults if not specified
    )
    logger.info(f"Created {chain_type} chain")
    
    # Interactive query loop
    print("\n" + "="*70)
    print("Ready to answer NIS-2 compliance questions!")
    print("="*70)
    print("Type your questions below (or 'quit' to exit)")
    print()
    
    while True:
        try:
            question = input("Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
            
            if not question:
                continue
            
            print("\nProcessing...")
            response = chain({"query": question})
            
            print("\n" + "-"*70)
            formatted_response = format_retrieval_response(response)
            print(formatted_response)
            print("-"*70 + "\n")
            
            logger.info(f"Answered question: {question[:50]}...")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            print(f"\nError: {e}\n")
    
    logger.info("NIS-2 Compliance Expert System shutting down")
    return 0


if __name__ == "__main__":
    sys.exit(main())
