from data.types import Data,TextType
from core.chunker import Chunking
from core.encoder import AzureOpenAIEncoder
from core.vectordb import QdrantDB
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


    def index(self,path):

        with open(path,"r") as file:
            text = file.read()

        doc_id = uuid.uuid5(uuid.NAMESPACE_DNS,path).hex
        data = Data(type = TextType.INDEX,text = text,id=doc_id)

        chunker = Chunking(chunk_size=500,overlap=100) 
        data = chunker(data) 

        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        data = encoder(data)

        db = QdrantDB() 
        data = db.as_indexer(data,collection_name='CLG')
        return {"message" : "Successfully index the document"}

    def doc_summary(self,doc):

        text = doc.text 

        #TO-DO use llm to summary 

    



