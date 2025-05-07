from core.vectordb import QdrantDB
from core.encoder import AzureOpenAIEncoder,OpenEncoder
from core.prompt import AugmentPrompt,CodePrompt
from core.llm import AzureGPTLLM, OpenRouterLLM
from data.types import Data,TextType
from core.constants import *

from data.psql import Postgres
from data.queries import *

import logging 
import uuid

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
        email = req['user_email'] 
        psql = Postgres() 
        user_data = psql.select_query(SELECT_USER_QUERY, (email,))
        user_id = user_data[0][0] # unique user id  

        collection_data = psql.select_query(SELECT_COLLECTION_QUERY,(user_id,))
        collection_name = collection_data[0][2]
        summary_collection_name = collection_data[0][3]
        
        unique_collection_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, email + collection_name))
        unique_summary_collection_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, email + summary_collection_name))

        return self.chat(req['query'],unique_collection_name, unique_summary_collection_name)