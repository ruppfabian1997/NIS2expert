"""
Retrieval chains for NIS-2 compliance queries.
Implements RetrievalQA and ConversationalRetrievalChain patterns.
"""

from typing import Optional, Dict, Any
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.llms.base import BaseLLM
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.base import VectorStore
from langchain.prompts import PromptTemplate


def get_retrieval_chain(
    vectorstore: VectorStore,
    chain_type: str = "retrieval_qa",
    llm: Optional[BaseLLM] = None,
    **kwargs
):
    """
    Create a retrieval chain for answering questions based on documents.
    
    Args:
        vectorstore: Vector store containing indexed documents
        chain_type: Type of chain ("retrieval_qa" or "conversational_retrieval")
        llm: Language model to use (defaults to GPT-3.5-turbo)
        **kwargs: Additional chain-specific arguments
        
    Returns:
        Configured retrieval chain
        
    Raises:
        ValueError: If chain_type is not supported
    """
    if llm is None:
        llm = _get_default_llm()
    
    chain_type = chain_type.lower()
    
    if chain_type == "retrieval_qa":
        return _create_retrieval_qa_chain(vectorstore, llm, **kwargs)
    elif chain_type == "conversational_retrieval":
        return _create_conversational_chain(vectorstore, llm, **kwargs)
    else:
        raise ValueError(
            f"Unsupported chain type: {chain_type}. "
            f"Supported types: retrieval_qa, conversational_retrieval"
        )


def _get_default_llm(
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.0,
    max_tokens: int = 500
) -> BaseLLM:
    """
    Get default language model.
    
    Args:
        model: Model identifier
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
        
    Returns:
        ChatOpenAI instance
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _create_retrieval_qa_chain(
    vectorstore: VectorStore,
    llm: BaseLLM,
    search_kwargs: Optional[Dict[str, Any]] = None,
    chain_type: str = "stuff",
    return_source_documents: bool = True,
    **kwargs
) -> RetrievalQA:
    """
    Create a RetrievalQA chain.
    
    Args:
        vectorstore: Vector store for retrieval
        llm: Language model
        search_kwargs: Arguments for similarity search (e.g., {'k': 4})
        chain_type: Chain type ("stuff", "map_reduce", "refine", "map_rerank")
        return_source_documents: Whether to return source documents
        **kwargs: Additional RetrievalQA arguments
        
    Returns:
        RetrievalQA chain instance
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}
    
    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    # TODO: Add NIS-2 specific prompt template
    # Custom prompt that guides the model to:
    # - Focus on compliance requirements
    # - Cite specific articles and sections
    # - Distinguish between mandatory and recommended measures
    # - Highlight implementation deadlines
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=return_source_documents,
        **kwargs
    )
    
    return qa_chain


def _create_conversational_chain(
    vectorstore: VectorStore,
    llm: BaseLLM,
    search_kwargs: Optional[Dict[str, Any]] = None,
    return_source_documents: bool = True,
    **kwargs
) -> ConversationalRetrievalChain:
    """
    Create a ConversationalRetrievalChain for multi-turn conversations.
    
    Args:
        vectorstore: Vector store for retrieval
        llm: Language model
        search_kwargs: Arguments for similarity search
        return_source_documents: Whether to return source documents
        **kwargs: Additional ConversationalRetrievalChain arguments
        
    Returns:
        ConversationalRetrievalChain instance
    """
    if search_kwargs is None:
        search_kwargs = {"k": 4}
    
    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    
    # TODO: Add NIS-2 specific conversation handling
    # - Maintain context of compliance domain being discussed
    # - Track which articles/requirements have been covered
    # - Provide progressive disclosure of information
    # - Handle follow-up questions about implementation details
    
    conv_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=return_source_documents,
        **kwargs
    )
    
    return conv_chain


def create_nis2_prompt_template() -> PromptTemplate:
    """
    Create NIS-2 specific prompt template.
    
    TODO: Implement custom prompt template for NIS-2 compliance queries
    
    The prompt should:
    - Instruct the model to act as a NIS-2 compliance expert
    - Emphasize accuracy and citation of sources
    - Request structured responses (requirements, deadlines, scope)
    - Guide towards actionable recommendations
    
    Returns:
        PromptTemplate configured for NIS-2 compliance
    """
    template = """
    You are a NIS-2 compliance expert assistant. Use the following pieces of context 
    from NIS-2 directive and ENISA guidelines to answer the question.
    
    If you don't know the answer based on the provided context, say so. 
    Do not make up information about compliance requirements.
    
    When citing requirements, always reference the specific article or section.
    
    Context: {context}
    
    Question: {question}
    
    Answer:
    """
    
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )


# TODO: NIS-2 specific chain enhancements
# - create_gap_analysis_chain(): Chain for identifying compliance gaps
# - create_scoring_chain(): Chain for scoring compliance level
# - create_recommendation_chain(): Chain for generating recommendations
# - create_audit_chain(): Chain for audit trail generation
# - create_report_chain(): Chain for compliance report generation
