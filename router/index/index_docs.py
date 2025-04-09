import uuid
import logging

from data.types import Data,TextType
from core.chunker import Chunking
from core.encoder import AzureOpenAIEncoder
from core.llm import AzureGPTLLM
from core.vectordb import QdrantDB
from core.constants import *
from core.prompt import SummarizerPrompt,CodextractorPrompt

class IndexDocs:
    def __init__(self) -> None:
        pass

    def index(self, path, collection_name, summary_collection_name):

        with open(path,"r") as file:
            text = file.read()

        doc_id = uuid.uuid5(uuid.NAMESPACE_DNS,path).hex
        data = Data(type = TextType.INDEX, content = text, id=doc_id)

        chunker = Chunking(chunk_size=500,overlap=100) 
        chunked_data = chunker(data) 

        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        embeded_data = encoder(chunked_data)

        db = QdrantDB() 
        db.as_indexer(embeded_data, collection_name=collection_name)

        self.doc_summary(data, summary_collection_name)
        return {"response" : "Successfully index the document"}

    def doc_summary(self, data:Data, summary_collection_name):

        summarizer = SummarizerPrompt()
        data = summarizer.generate_prompt(data)

        #llm to summary the whole document 
        llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        data = llm(data)
        summary = data.metadata[RESPONSE]

        with open("test.txt","w") as file:
            file.write(summary)

        codeExtractor = CodextractorPrompt()
        data = codeExtractor.generate_prompt(data)

        #llm to extract the code from document
        data = llm(data)
        data.metadata[CODE] = data.metadata[RESPONSE]
        data.persist_to_db.append(CODE)

        with open("test.txt","+a") as file:
            file.write("\n" "_"*100+"\n" + data.metadata[CODE])
        
        #replace the whole document text  with its summary
        data.content = summary
        data.parent = True

        db = QdrantDB()
        db.as_indexer(data, collection_name=summary_collection_name)
        logging.info("Successfully index the doc summary")
    
    def __call__(self, req:dict):
        return self.index(req['path'], req['collection_name'], req.get('summary_collection_name') or DEFAULT_SUMMARY_COLLECTION_NAME)
