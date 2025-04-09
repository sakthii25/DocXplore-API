from fastapi import FastAPI,Request,HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import os
from router.index.index_docs import IndexDocs 
from router.query.chat_docs import ChatDocs
from router.helper_functions import create_collections,delete_collections,AtlasClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('URI')
database = os.getenv('DATABASE')
collection_name = os.getenv('COLLECTION_NAME')

app = FastAPI()
db = AtlasClient(uri,database)


class IndexDoc(BaseModel):
    path: str 
    collection_name: str 

class QueryDoc(BaseModel):
    query: str 
    collection_name: str 

class Collection(BaseModel):
    collection_name: str 

@app.get("/")
def root():
    return {"message" : "Hello World!"}

@app.get("/health")
def health_check():
    return {"response": "ok"} 

# @app.middleware('http')
# def middleware(req: Request,call_next):
#     path = req.url.path 
#     if path in ["/","/health"]:
#         res = call_next(req) 
#         return res 
    
#     api_key = req.headers.get('API_KEY')
#     check = db.find(collection_name,{'key': api_key})
#     if check is None:
#         raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
#     res = call_next(req) 
#     return res

@app.post("/index-docs")
def index(req:IndexDoc):
    index = IndexDocs()
    res = index(req.model_dump())
    return JSONResponse(res)

@app.post("/query-docs")
def query(req:QueryDoc):
    chat = ChatDocs()
    res = chat(req.model_dump())
    return JSONResponse(res)

@app.get("/create-collection")
def create_collection(req:Collection):
    res = create_collections(req.model_dump())
    return JSONResponse(res)

@app.get("/delete-collection")
def delete_collection(req:Collection):
    res = delete_collections(req.model_dump())
    return JSONResponse(res)

if __name__ == "__main__":
    uvicorn.run(app)