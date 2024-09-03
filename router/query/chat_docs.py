from core.vectordb import QdrantDB
from core.encoder import AzureOpenAIEncoder
from core.prompt import AugmentPrompt
from core.llm import AzureGPTLLM
from data.types import Data,TextType
import os

AZURE_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")
AZURE_EMB_DEPLOYMENT_NAME = os.getenv("AZURE_EMB_DEPLOYMENT_NAME")
AZURE_BASE_URL = os.getenv("AZURE_BASE_URL") 
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

class ChatDocs:
    def __init__(self) -> None:
        pass

    def chat(self,query,collection_name):

        query = Data(type=TextType.QUERY,content=query)
        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        query = encoder(query)

        db = QdrantDB()
        query = db.as_retriever(query,collection_name=collection_name)

        prompt = AugmentPrompt()
        query = prompt(query)

        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        query = llm(query)

        return query

    def __call__(self, req:dict):
        return self.chat(req['query'],req['collection_name'])

    