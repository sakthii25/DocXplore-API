import logging
from pymongo import MongoClient
from qdrant_client.models import VectorParams,Distance

from core.vectordb import QdrantDB
from core.constants import *

def create_collections(request: dict):

    logger = logging.getLogger("router")

    main_collection_name = request["collection_name"]
    summary_collection_name = request.get("summary_collection_name") or DEFAULT_SUMMARY_COLLECTION_NAME
    vector_name = request.get("vector_name") or DEFAULT_VECTOR_NAME

    vector_configuration = {
        vector_name: VectorParams(size=1536, distance=Distance.COSINE)
    }

    qdrant_database = QdrantDB()
    qdrant_database.create_collection(
        collection_name=main_collection_name,
        vectors_config=vector_configuration
    )
    logger.info(f"Main collection '{main_collection_name}' created successfully.")
    qdrant_database.create_collection(
        collection_name=summary_collection_name,
        vectors_config=vector_configuration
    )
    logger.info(f"Summary collection '{summary_collection_name}' created successfully.")

    return {"message": "Collections created successfully"}

def delete_collections(request: dict):
    logger = logging.getLogger(__name__)

    main_collection_name = request['collection_name']
    summary_collection_name = request.get("summary_collection_name") or DEFAULT_SUMMARY_COLLECTION_NAME
    
    db = QdrantDB()
    db.delete_collection(collection_name=main_collection_name)
    logger.info(f"Main collection '{main_collection_name}' deleted successfully.")
    db.delete_collection(collection_name=summary_collection_name)
    logger.info(f"Summary collection '{summary_collection_name}' deleted successfully.")

    return {"message" : "Successfully deleted the collection"}

class AtlasClient ():

   def __init__ (self, altas_uri, dbname):
       self.mongodb_client = MongoClient(altas_uri)
       self.database = self.mongodb_client[dbname]

   ## A quick way to test if we can connect to Atlas instance
   def ping (self):
       self.mongodb_client.admin.command('ping')

   def get_collection (self, collection_name):
       collection = self.database[collection_name]
       return collection
   
   def insert(self,collection_name,document):
       collection = self.database[collection_name]
       return collection.insert_one(document)

   def find(self, collection_name, filter = {}):
       collection = self.database[collection_name]
       item = collection.find_one(filter=filter)
       return item