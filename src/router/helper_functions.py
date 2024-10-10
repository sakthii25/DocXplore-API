from src.core.vectordb import QdrantDB
from pymongo import MongoClient
from qdrant_client.models import VectorParams,Distance

def create_collections(req:dict):

    collection_name = req['collection_name']
    vector_config ={
        "text_dense_vec": VectorParams(size=1536, distance=Distance.COSINE)
    }
    db = QdrantDB()
    db.create_collection(collection_name=collection_name,vectors_config = vector_config)

    return {"message" : "Successfully created the collection"}


def delete_collections(req:dict):
    collection_name = req['collection_name']
    
    db = QdrantDB()
    db.delete_collection(collection_name=collection_name)

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
   