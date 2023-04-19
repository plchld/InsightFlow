# retrieval_qa.py

from lib.chat.setup import llm, llm4
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate

def setup_retrieval_qa(vectordb):
    prompt_template = """
    
    You are a world class notetaker with over 30 years of experience in 
    taking notes and answering questions based on those notes. 
    Your one purpose in life is to truthfully answer the 
    questions of the user about their notes.\\n
    Use the following pieces of context to answer the question at the end. \\n
   
    {context}

    Question: {question}

    notetaker's answer :"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    chain_type_kwargs = {"prompt": PROMPT}

    retriever = vectordb.as_retriever()
    qa = RetrievalQA.from_chain_type(llm4, chain_type="stuff", retriever=retriever, return_source_documents=False)
    return qa
