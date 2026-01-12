"""
LangChain chains for NIS-2 compliance queries and analysis.

This module provides pre-configured chains for question answering,
document analysis, and compliance-related tasks.
"""

from typing import Any, Dict, List, Optional

from langchain.chains import RetrievalQA
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class NIS2Chain:
    """
    Base class for NIS-2 compliance chains.
    
    Provides common functionality for creating and configuring LangChain chains
    for compliance-related tasks.
    """
    
    def __init__(
        self,
        llm_model: Optional[str] = None,
        temperature: Optional[float] = None,
        openai_api_key: Optional[str] = None,
    ):
        """
        Initialize the chain.
        
        Args:
            llm_model: LLM model to use
            temperature: Temperature for response generation
            openai_api_key: OpenAI API key
        """
        from nis2expert.config import get_settings
        
        settings = get_settings()
        self.model = llm_model or settings.llm_model
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self.api_key = openai_api_key or settings.openai_api_key
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set NIS2_OPENAI_API_KEY environment variable "
                "or provide it in .env file"
            )
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=self.api_key,
        )


class NIS2QAChain(NIS2Chain):
    """
    Question-Answering chain for NIS-2 compliance documents.
    
    Provides context-aware answers to questions about NIS-2 regulations
    and compliance requirements using retrieval-augmented generation.
    """
    
    DEFAULT_PROMPT_TEMPLATE = """You are an expert on NIS-2 (Network and Information Security Directive) and ENISA compliance.
Use the following pieces of context from official NIS-2 and ENISA documents to answer the question at the end.

If you don't know the answer based on the provided context, just say that you don't know. Don't try to make up an answer.
Always cite the specific article, section, or document when providing answers.

Context:
{context}

Question: {question}

Answer:"""
    
    def __init__(
        self,
        retriever,
        prompt_template: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the QA chain.
        
        Args:
            retriever: Document retriever instance
            prompt_template: Custom prompt template
            **kwargs: Additional arguments for NIS2Chain
        """
        super().__init__(**kwargs)
        
        self.retriever = retriever
        self.prompt = PromptTemplate(
            template=prompt_template or self.DEFAULT_PROMPT_TEMPLATE,
            input_variables=["context", "question"],
        )
        
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt},
        )
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the QA chain with a query.
        
        Args:
            query: Question to answer
            
        Returns:
            Dictionary with 'result' and 'source_documents'
        """
        return self.chain({"query": query})
    
    def __call__(self, query: str) -> Dict[str, Any]:
        """Allow calling the chain directly."""
        return self.run(query)


class ComplianceCheckChain(NIS2Chain):
    """
    Chain for checking compliance against NIS-2 requirements.
    
    Analyzes organizational practices or controls against NIS-2 requirements
    to identify compliance status and gaps.
    """
    
    COMPLIANCE_PROMPT_TEMPLATE = """You are a NIS-2 compliance auditor. Based on the following NIS-2 requirements and the organization's current practices, assess the compliance status.

NIS-2 Requirements:
{requirements}

Organization's Current Practices:
{practices}

Provide a structured compliance assessment including:
1. Compliance Status (Compliant/Partially Compliant/Non-Compliant)
2. Specific gaps or issues identified
3. Recommendations for achieving full compliance

Assessment:"""
    
    def __init__(
        self,
        retriever,
        prompt_template: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the compliance check chain.
        
        Args:
            retriever: Document retriever for NIS-2 requirements
            prompt_template: Custom prompt template
            **kwargs: Additional arguments for NIS2Chain
        """
        super().__init__(**kwargs)
        
        self.retriever = retriever
        self.prompt = PromptTemplate(
            template=prompt_template or self.COMPLIANCE_PROMPT_TEMPLATE,
            input_variables=["requirements", "practices"],
        )
        
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def check_compliance(
        self,
        topic: str,
        current_practices: str,
    ) -> str:
        """
        Check compliance for a specific topic.
        
        Args:
            topic: Compliance topic or requirement area
            current_practices: Description of current organizational practices
            
        Returns:
            Compliance assessment
        """
        # Retrieve relevant requirements
        requirements_docs = self.retriever.get_relevant_documents(topic)
        requirements_text = "\n\n".join([doc.page_content for doc in requirements_docs])
        
        # Run compliance check
        result = self.llm_chain.run(
            requirements=requirements_text,
            practices=current_practices,
        )
        
        return result


class DocumentSummaryChain(NIS2Chain):
    """
    Chain for summarizing NIS-2 documents or sections.
    
    Provides concise summaries of regulatory documents, articles, or sections
    while preserving key compliance requirements.
    """
    
    SUMMARY_PROMPT_TEMPLATE = """Provide a concise summary of the following NIS-2 regulatory text.
Focus on key requirements, obligations, and compliance implications.

Text:
{text}

Summary:"""
    
    def __init__(
        self,
        prompt_template: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the summary chain.
        
        Args:
            prompt_template: Custom prompt template
            **kwargs: Additional arguments for NIS2Chain
        """
        super().__init__(**kwargs)
        
        self.prompt = PromptTemplate(
            template=prompt_template or self.SUMMARY_PROMPT_TEMPLATE,
            input_variables=["text"],
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def summarize(self, text: str) -> str:
        """
        Summarize a document or text.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
        """
        return self.chain.run(text=text)
    
    def summarize_documents(self, documents: List) -> str:
        """
        Summarize a list of documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Combined summary
        """
        combined_text = "\n\n".join([doc.page_content for doc in documents])
        return self.summarize(combined_text)
