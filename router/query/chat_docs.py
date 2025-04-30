from core.vectordb import QdrantDB
from core.encoder import AzureOpenAIEncoder,OpenEncoder
from core.prompt import AugmentPrompt,CodePrompt
from core.llm import AzureGPTLLM, OpenRouterLLM
from data.types import Data,TextType
from core.constants import *

import logging 

logger = logging.getLogger("router")
class ChatDocs:
    def __init__(self) -> None:
        pass

    def chat(self, query, collection_name, summary_collection_name):

        query = Data(type=TextType.QUERY, content=query)
        
        # if FREE_VERSION :
        #     encoder = OpenEncoder(model=FREE_EMB_MODEL)
        # else:
        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)

        query = encoder(query)
        # logger.info(f"User query is encoded using {"openEncoder" if FREE_VERSION else "azureEncoder"}")

        db = QdrantDB()
        query = db.as_retriever(query, collection_name=collection_name)

        prompt = AugmentPrompt()
        query = prompt(query, summary_collection_name)

        #llm call to give the holistic overview of the question 
        if FREE_VERSION :
           llm = OpenRouterLLM(api_key=OPEN_ROUTER_API_KEY)
        else: 
            llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)

        query = llm(query)
        # logger.info(f"{"openRouterLLM" if FREE_VERSION else "azureGPTLLM"} is using for the query")

        prompt = CodePrompt()
        query = prompt(query, summary_collection_name)

        #Stream llm Response
        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY,stream=True)

        #llm call to give the code part for the question
        query = llm(query)

        return query.metadata[RESPONSE]

    def __call__(self, req:dict):
        return self.chat(req['query'],req['collection_name'], req.get('summary_collection_name') or DEFAULT_SUMMARY_COLLECTION_NAME)