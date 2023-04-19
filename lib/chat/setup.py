import openai
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from lib.config import Config


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=Config.chat_temp, openai_api_key=Config.openai_key)
llm4 = ChatOpenAI(model_name="gpt-4", temperature=Config.gpt4_temp, openai_api_key=Config.openai_key)
openai.api_key = Config.openai_key

cohere = CohereEmbeddings(model="large", cohere_api_key=Config.cohere_key)
