import openai
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from lib.config import Config


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=Config.chat_temp, openai_api_key=Config.openai_key)
llm4 = ChatOpenAI(model_name="gpt-4", temperature=Config.gpt4_temp, openai_api_key=Config.openai_key)
#not sure if this is needed if i pass it in config
openai.api_key = Config.openai_key

openai_embeddings = OpenAIEmbeddings(openai_api_key = Config.openai_key)