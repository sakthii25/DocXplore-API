import uuid
import logging

from data.types import Data,TextType
from core.chunker import Chunking
from core.encoder import AzureOpenAIEncoder, OpenEncoder
from core.llm import AzureGPTLLM, OpenRouterLLM
from core.vectordb import QdrantDB
from core.constants import *
from core.prompt import SummarizerPrompt,CodextractorPrompt

from data.psql import Postgres
from data.queries import *

logger = logging.getLogger("router")

class IndexDocs:
    def __init__(self) -> None:
        pass

    def index(self, content, collection_name, summary_collection_name, meta_data):

        doc_id = uuid.uuid4().hex
        data = Data(type = TextType.INDEX, content = content, id=doc_id)

        chunker = Chunking(chunk_size=500,overlap=100) 
        chunked_data = chunker(data) 

        # if FREE_VERSION :
        #     encoder = OpenEncoder(model=FREE_EMB_MODEL)
        # else:
        encoder = AzureOpenAIEncoder(deployment_name=AZURE_EMB_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)
        
        embeded_data = encoder(chunked_data)
        # logger.info(f"Document is encoded using {"openEncoder" if FREE_VERSION else "azureEncoder"}")

        db = QdrantDB() 
        db.as_indexer(embeded_data, collection_name=collection_name)
        logger.info("Sucessfully index the collection 1")

        self.doc_summary(data, summary_collection_name)

        psql = Postgres()
        psql.insert_query(INSERT_QUERY,(doc_id, meta_data['document_name'], meta_data['document_size'], meta_data['uploaded_date']))
        psql.close()

        meta_data['id'] = doc_id

        return meta_data

    def doc_summary(self, data:Data, summary_collection_name):

        summarizer = SummarizerPrompt()
        data = summarizer.generate_prompt(data)

        #llm to summary the whole document 

        if FREE_VERSION :
           llm = OpenRouterLLM(api_key=OPEN_ROUTER_API_KEY)
        else: 
            llm = AzureGPTLLM(deployment_name=AZURE_GPT_DEPLOYMENT_NAME,api_base=AZURE_BASE_URL,api_version=AZURE_API_VERSION,api_key=AZURE_API_KEY)

        data = llm(data)
        summary = data.metadata[RESPONSE]

        codeExtractor = CodextractorPrompt()
        data = codeExtractor.generate_prompt(data)

        #llm to extract the code from document
        data = llm(data)
        data.metadata[CODE] = data.metadata[RESPONSE]
        data.persist_to_db.append(CODE)
        
        #replace the whole document text  with its summary
        data.content = summary
        data.parent = True

        db = QdrantDB()
        db.as_indexer(data, collection_name=summary_collection_name)
        logger.info("Successfully index the document summary and their code")
    
    def __call__(self, req:dict):
        return self.index(req['content'], req['collection_name'], req.get('summary_collection_name') or DEFAULT_SUMMARY_COLLECTION_NAME, req['document_data'])