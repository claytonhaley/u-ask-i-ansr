import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import Runnable
from langchain.vectorstores.base import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

def setup_chains(retriever: VectorStoreRetriever) -> Runnable:
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_template = ChatPromptTemplate.from_template("""
    Given comments from the YouTube video titled '{title}', answer the question given the context. 
    <context>
    {context}
    </context>
    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)
    retrieval_chain = create_retrieval_chain(retriever, document_chain) | prompt_template | llm | StrOutputParser()

    return retrieval_chain