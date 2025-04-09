import os
import logging
import uvicorn

from pydantic import BaseModel
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import Optional

from router.index.index_docs import IndexDocs 
from router.query.chat_docs import ChatDocs
from router.helper_functions import *
from data.types import *

# NOT NEEDED NOW
# load_dotenv()
# uri = os.getenv('URI')
# database = os.getenv('DATABASE')
# collection_name = os.getenv('COLLECTION_NAME')

app = FastAPI()
# db = AtlasClient(uri,database)

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

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()  # for terminal
        ]
    )

configure_logging()

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_level="info")