from core.vectordb import QdrantDB
from core.encoder import AzureOpenAIEncoder
from core.prompt import AugmentPrompt,CodePrompt
from core.llm import AzureGPTLLM
from data.types import Data,TextType
from core.constants import *
import os

class ChatDocs:
    def __init__(self) -> None:
        pass

    def chat(self, query, collection_name, summary_collection_name):

        query = Data(type=TextType.QUERY, content=query)
        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        query = encoder(query)

        db = QdrantDB()
        query = db.as_retriever(query, collection_name=collection_name)

        prompt = AugmentPrompt()
        query = prompt(query, summary_collection_name)

        #llm call to give the holistic overview of the question 
        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        query = llm(query)

        prompt = CodePrompt()
        query = prompt(query, summary_collection_name)

        #llm call to give the code part for the question
        query = llm(query)

        response = query.metadata[RESPONSE]
        return {"response" : response}

    def __call__(self, req:dict):
        return self.chat(req['query'],req['collection_name'], req.get('summary_collection_name') or DEFAULT_SUMMARY_COLLECTION_NAME)