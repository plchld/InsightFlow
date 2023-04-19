# setup.py
import openai
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
import local_settings


from local_settings import OPENAI_API_KEY, CHAT_MODEL_TEMPERATURE, GPT_4_TEMPERATURE, COHERE_API_KEY

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=CHAT_MODEL_TEMPERATURE, openai_api_key=OPENAI_API_KEY)
llm4 = ChatOpenAI(model_name="gpt-4", temperature=GPT_4_TEMPERATURE, openai_api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

cohere = CohereEmbeddings(model="large", cohere_api_key=COHERE_API_KEY)
