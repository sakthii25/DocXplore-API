from qdrant_client import QdrantClient
from qdrant_client.models import  PointStruct
from data.types import Data

class QdrantDB:

    def __init__(self, host: str = "http://localhost", port:str=6333, verbose=True):
            self.url = f"{host}:{port}"
            self.client = self._create_client()
            self.verbose = verbose

    
    def _create_client(self) -> 'QdrantClient':
        try:
            return QdrantClient(url=self.url)
        except Exception as e:
            print(f"Failed to create QdrantClient: {e}")
            return None
        
    def create_collection(self,collection_name:str,**kwargs):
        if not self.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                **kwargs
            )

    def collection_exists(self,collection_name):
        return self.client.collection_exists(collection_name)
    
    def get_payload(self,data:Data):
        payload = {}
        payload['text'] = data.text 
        payload['parent_docid'] = data.id
        for key, value in data.metadata.items():
            payload[key] = value
        return payload
    
    def process_data(self,data:Data):

        points = []
        for data in data:
           point_id = data.metadata.get('chunk_id', data.id)
           vectors = {}
           vectors["text_dense_vec"] = data.vectors
           payload = self.get_payload(data)
           point = PointStruct(id=point_id,vector=vectors,payload=payload)
           points.append(point)

        return points
    
    def upload_points(self, collection_name, vectors, batch_size=64):
        try:
            operation_info = self.client.upload_points(
                collection_name=collection_name,
                points=vectors,
                batch_size=batch_size,
                wait=True
            )
            return operation_info
        except Exception as ex:
             raise Exception(f"Exception while inserting point in {collection_name}")
    

    def as_indexer(self,data:Data,collection_name = None):

        if collection_name is None or not self.client.collection_exists(collection_name):
            raise Exception(f"Collection {collection_name} does not exist")
        
        try:
            if not isinstance(data, list):
                data = [data]

            data=self.process_data(data)
            self.upload_points(collection_name, data)
        except Exception as ex:
            raise ex

