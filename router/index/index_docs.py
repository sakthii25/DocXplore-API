from data.types import Data,TextType
from core.chunker import Chunking
from core.encoder import AzureOpenAIEncoder
from core.llm import AzureGPTLLM
from core.vectordb import QdrantDB
from core.prompt import SummarizerPrompt
import uuid
import os


AZURE_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")
AZURE_EMB_DEPLOYMENT_NAME = os.getenv("AZURE_EMB_DEPLOYMENT_NAME")
AZURE_BASE_URL = os.getenv("AZURE_BASE_URL") 
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")

class IndexDocs:
    def __init__(self) -> None:
        pass


    def index(self,path,collection_name):

        with open(path,"r") as file:
            text = file.read()

        doc_id = uuid.uuid5(uuid.NAMESPACE_DNS,path).hex
        data = Data(type = TextType.INDEX,content = text,id=doc_id)

        chunker = Chunking(chunk_size=500,overlap=100) 
        chunked_data = chunker(data) 

        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        embeded_data = encoder(chunked_data)

        db = QdrantDB() 
        db.as_indexer(embeded_data,collection_name=collection_name)

        self.doc_summary(data)
        return {"response" : "Successfully index the document"}

    def doc_summary(self,data:Data):

        print(data.metadata)
        prompt = SummarizerPrompt()
        data = prompt(data)

        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        data = llm(data)
        data.content = data.metadata['response']

        db = QdrantDB()
        db.as_indexer(data,collection_name='doc summary')
        print("Successfully index the doc summary")
    
    def __call__(self, req:dict):
        return self.index(req['path'],req['collection_name'])


    



