"""
Example usage of NIS2expert system.

This script demonstrates how to use the NIS2expert package for:
- Loading NIS-2 documents
- Creating embeddings and vector stores
- Performing question answering
- Running compliance checks
"""

import os
from pathlib import Path

from nis2expert.config import get_settings
from nis2expert.loaders import NIS2DocumentLoader
from nis2expert.splitters import NIS2TextSplitter
from nis2expert.embeddings import get_embeddings
from nis2expert.vectorstore import NIS2VectorStore
from nis2expert.chains import NIS2QAChain, ComplianceCheckChain
from nis2expert.utils import setup_logging


def main():
    """Run example NIS2expert workflow."""
    
    # Set up logging
    logger = setup_logging()
    logger.info("Starting NIS2expert example...")
    
    # Get settings
    settings = get_settings()
    logger.info(f"Using configuration: {settings.model_dump()}")
    
    # Check if API key is set
    if not settings.openai_api_key:
        logger.error(
            "OpenAI API key not found. Please set NIS2_OPENAI_API_KEY environment variable."
        )
        logger.info("You can create a .env file with: NIS2_OPENAI_API_KEY=your-key-here")
        return
    
    # 1. Load documents
    logger.info("Step 1: Loading documents...")
    loader = NIS2DocumentLoader()
    
    # Check if documents directory exists and has files
    if not settings.documents_dir.exists() or not any(settings.documents_dir.iterdir()):
        logger.warning(f"No documents found in {settings.documents_dir}")
        logger.info("Please add NIS-2/ENISA PDF or DOCX documents to the documents directory.")
        logger.info("Creating sample document for demonstration...")
        
        # Create a sample document for demonstration
        sample_doc_path = settings.documents_dir / "sample_nis2_info.txt"
        sample_content = """
        NIS-2 Directive - Network and Information Security
        
        The NIS-2 Directive is the EU-wide legislation on cybersecurity. It provides legal 
        measures to boost the overall level of cybersecurity in the EU.
        
        Key Requirements:
        - Risk management measures
        - Corporate accountability
        - Reporting obligations
        - Business continuity
        - Supply chain security
        - Security in network and information systems acquisition, development and maintenance
        """
        sample_doc_path.write_text(sample_content)
        logger.info(f"Created sample document: {sample_doc_path}")
    
    try:
        documents = loader.load_directory(show_progress=True)
        logger.info(f"Loaded {len(documents)} documents")
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        return
    
    if not documents:
        logger.warning("No documents were loaded. Exiting.")
        return
    
    # 2. Split documents
    logger.info("Step 2: Splitting documents into chunks...")
    splitter = NIS2TextSplitter()
    chunks = splitter.split_documents(documents)
    logger.info(f"Created {len(chunks)} chunks")
    
    # 3. Create embeddings
    logger.info("Step 3: Creating embeddings...")
    try:
        embeddings = get_embeddings()
    except Exception as e:
        logger.error(f"Error creating embeddings: {e}")
        return
    
    # 4. Create vector store
    logger.info("Step 4: Creating vector store...")
    vectorstore_manager = NIS2VectorStore()
    
    try:
        # Try to load existing vector store
        logger.info("Attempting to load existing vector store...")
        vectorstore = vectorstore_manager.load_vectorstore(embeddings)
        logger.info("Loaded existing vector store")
    except (FileNotFoundError, Exception) as e:
        logger.info(f"Creating new vector store: {e}")
        vectorstore = vectorstore_manager.create_vectorstore(chunks, embeddings)
        logger.info("Created new vector store")
    
    # 5. Create retriever
    logger.info("Step 5: Creating retriever...")
    retriever = vectorstore_manager.as_retriever()
    
    # 6. Question Answering
    logger.info("\n" + "="*60)
    logger.info("Step 6: Question Answering Example")
    logger.info("="*60)
    
    qa_chain = NIS2QAChain(retriever=retriever)
    
    example_questions = [
        "What are the main requirements of NIS-2?",
        "What are the reporting obligations under NIS-2?",
        "What security measures are required?",
    ]
    
    for question in example_questions:
        logger.info(f"\nQuestion: {question}")
        try:
            result = qa_chain.run(question)
            logger.info(f"Answer: {result['result']}")
            logger.info(f"Source documents: {len(result.get('source_documents', []))}")
        except Exception as e:
            logger.error(f"Error answering question: {e}")
    
    # 7. Compliance Check Example
    logger.info("\n" + "="*60)
    logger.info("Step 7: Compliance Check Example")
    logger.info("="*60)
    
    compliance_chain = ComplianceCheckChain(retriever=retriever)
    
    example_practice = """
    Our organization has implemented:
    - Annual security awareness training
    - Incident response plan with 48-hour reporting timeframe
    - Regular vulnerability scanning
    - Basic access controls
    """
    
    try:
        compliance_result = compliance_chain.check_compliance(
            topic="incident reporting and security measures",
            current_practices=example_practice,
        )
        logger.info(f"\nCompliance Assessment:\n{compliance_result}")
    except Exception as e:
        logger.error(f"Error in compliance check: {e}")
    
    logger.info("\n" + "="*60)
    logger.info("Example completed successfully!")
    logger.info("="*60)


if __name__ == "__main__":
    main()
