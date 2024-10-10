from src.data.types import Data,TextType
from src.core.chunker import Chunking
from src.core.encoder import AzureOpenAIEncoder
from src.core.llm import AzureGPTLLM
from src.core.vectordb import QdrantDB
from src.core.prompt import SummarizerPrompt,CodextractorPrompt
import logging
import uuid
import os

log = logging(__name__)

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

        prompt = SummarizerPrompt()
        data = prompt(data)

        #llm to summary the whole document 
        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        data = llm(data)
        summary = data.metadata['response']

        prompt = CodextractorPrompt()
        data = prompt(data)

        #llm to extract the code from document
        data = llm(data)
        data.metadata['code'] = data.metadata['response']
        data.persist_to_db.append('code')
        
        #replace the whole document text  with its summary
        data.content = summary

        db = QdrantDB()
        db.as_indexer(data,collection_name='doc summary')
        log.info("Successfully index the doc summary")
    
    def __call__(self, req:dict):
        path = req.get('path',None)
        collection_name = req.get('collection_name',None)
        return self.index(path,collection_name)


    



