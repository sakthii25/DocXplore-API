from core.vectordb import QdrantDB
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
