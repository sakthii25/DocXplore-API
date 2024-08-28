from data.types import Data,TextType
from core.chunker import Chunking
from core.encoder import AzureOpenAIEncoder

class IndexDocs:
    def __init__(self) -> None:
        pass


    def index(self,path):

        with open(path,"r") as file:
            text = file.read()

        data = Data(type = TextType.INDEX,text = text,metadata = {"doc_id" : 1})
        chunker = Chunking() 
        data = chunker(data) 

        encoder = AzureOpenAIEncoder()
        data = encoder(data)
        return {"message" : "Successfully index the document"}

    def doc_summary(self,doc):

        text = doc.text 

        #TO-DO use llm to summary 

    



