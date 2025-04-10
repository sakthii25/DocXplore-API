from typing import List
from data.types import Data
from openai import AzureOpenAI

from sentence_transformers import SentenceTransformer

class AzureOpenAIEncoder():
    def __init__(self, deployment_name=None, api_base=None, api_version=None, api_key=None) -> None:
        self.client = AzureOpenAI(
            azure_endpoint= api_base,
            azure_deployment= deployment_name,
            api_version= api_version,
            api_key= api_key
        )
        self.model_name = deployment_name

    def encode(self, data:Data):

        text = data.content
        emb = self.client.embeddings.create(input = text, model=self.model_name).data[0].embedding
        data.vectors = emb 

        return data
    
    def batch_encode(self,data):

        embeded_data = []
        for data in data:
            data = self.encode(data)
            embeded_data.append(data)
        
        return embeded_data

    def __call__(self, data):

        if isinstance(data, list):
            return self.batch_encode(data)
        else:
            return self.encode(data)


class OpenEncoder():
    def __init__(self, model = None) -> None:
        self.model = SentenceTransformer(model)
        pass

    def encode(self, data:Data):

        text = data.content
        # emb = self.client.embeddings.create(input = text, model=self.model_name).data[0].embedding
        emb = self.model.encode([text],normalize_embeddings=True)
        data.vectors = emb[0].tolist()

        return data
    
    def batch_encode(self,data):

        embeded_data = []
        for data in data:
            data = self.encode(data)
            embeded_data.append(data)
        
        return embeded_data

    def __call__(self, data):

        if isinstance(data, list):
            return self.batch_encode(data)
        else:
            return self.encode(data)