import logging
import uuid 
from pymongo import MongoClient
from qdrant_client.models import VectorParams,Distance

from core.vectordb import QdrantDB
from core.constants import *
from data.psql import *
from data.queries import *

def create_collections(request: dict):

    logger = logging.getLogger("router")
    psql = Postgres() 

    email = request["user_email"]
    main_collection_name = request["collection_name"]
    summary_collection_name = request.get("summary_collection_name") or DEFAULT_SUMMARY_COLLECTION_NAME
    vector_name = request.get("vector_name") or DEFAULT_VECTOR_NAME

    user_data = psql.select_query(SELECT_USER_QUERY, (email,)) # it return always list of 1 cuz email is unique
    print(user_data)
    print(type(user_data))
    user_id = user_data[0][0]
    print("userid: ",user_id)
    unique_collection_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, email + main_collection_name))
    unique_summary_collection_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, email + summary_collection_name))

    # if FREE_VERSION:
    #     EMB_SIZE = FREE_EMB_SIZE 
    # else:
    EMB_SIZE = OPENAI_EMB_SIZE

    vector_configuration = {
        vector_name: VectorParams(size=EMB_SIZE, distance=Distance.COSINE)
    }

    qdrant_database = QdrantDB()
    qdrant_database.create_collection(
        collection_name=unique_collection_name,
        vectors_config=vector_configuration
    )
    logger.info(f"Main collection '{main_collection_name}' created successfully.")
    qdrant_database.create_collection(
        collection_name=unique_summary_collection_name,
        vectors_config=vector_configuration
    )
    logger.info(f"Summary collection '{summary_collection_name}' created successfully.") 

    psql.insert_query(INSERT_COLLECTION_QUERY, (user_id, main_collection_name, summary_collection_name))
    psql.close()
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


def delete_document(req: dict):

    id = req['id']
    collection_name = req['collection_name']
    summary_collection_name = req['summary_collection_name']
    psql = Postgres() 
    psql.delete_query(DELETE_QUERY,(id,))
    psql.close()

    db = QdrantDB()
    db.delete_point(PARENT_ID,id,collection_name)
    db.delete_point(DOC_ID,id,summary_collection_name)

    return {"message" : "Successfully deleted the document"}

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