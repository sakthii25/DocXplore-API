from core.vectordb import QdrantDB
from qdrant_client.models import VectorParams,Distance

def create_collections(req:dict):

    collection_name = req['collection_name']
    vector_config = VectorParams(
                        size = 1536,
                        distance = Distance.COSINE
                    )
    db = QdrantDB()
    db.create_collection(collection_name=collection_name,vectors_config = vector_config)

    return {"message" : "Successfully created the collection"}
