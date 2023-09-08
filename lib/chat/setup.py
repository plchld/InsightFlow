import openai
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from lib.config import Config


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=Config.chat_temp, openai_api_key=Config.openai_key)
llm4 = ChatOpenAI(model_name="gpt-4", temperature=Config.gpt4_temp, openai_api_key=Config.openai_key)
gptAzure = AzureChatOpenAI(
    openai_api_base= Config.BASE_URL,
    openai_api_version="2023-05-15", 
    deployment_name=Config.DEPLOYMENT_NAME,
    openai_api_key=Config.AZURE_KEY,
    openai_api_type="azure",
)
#not sure if this is needed if i pass it in config
openai.api_key = Config.openai_key

openai_embeddings = OpenAIEmbeddings(openai_api_key = Config.openai_key)