import os
import json
import logging
import uvicorn
import datetime

from pydantic import BaseModel
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from router.index.index_docs import IndexDocs 
from router.query.chat_docs import ChatDocs
from router.helper_functions import *
from data.types import *
from data.queries import * 
from data.psql import Postgres
import markdown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

COLUMN_NAMES = ["id", "document_name", "document_size", "uploaded_date"]

def serialize_row(row: tuple) -> dict:
    data = dict(zip(COLUMN_NAMES, row))
    data["uploaded_date"] = data["uploaded_date"].date().isoformat()

    return data

@app.get("/list-documents")
def get_documents():
    psql = Postgres()
    rows = psql.select_query(SELECT_QUERY)
    psql.close()
    sorted_rows = sorted(rows, key=lambda row: row[3], reverse=True)
    result = [serialize_row(row) for row in sorted_rows]
    return JSONResponse(content={"result": result})

@app.post("/delete-document")
def del_document(req: Document):
    res = delete_document(req.model_dump())
    return JSONResponse(res)
    
def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    
@app.post("/index-docs")
async def index(
    file: UploadFile = File(...),
    json_str: str = Form(...)
):
    content = await file.read()
    size_str = format_file_size(file.size)
    
    json_data = json.loads(json_str)
    json_data["content"] = content
    json_data["document_data"] = {
        "document_name": file.filename,
        "document_size": size_str,
        "uploaded_date": datetime.date.today()
    }
    index = IndexDocs()
    result = index(json_data)
    result['uploaded_date'] = result["uploaded_date"].isoformat()
    return JSONResponse(content=result)
   

def is_valid_markdown(md_text):
    try: 
        html = markdown.markdown(md_text)
        return True
    except Exception:
        return False
  
def stream_processor(response):
    buffer = ""
    for chunk in response:
        if len(chunk.choices) > 0:
            delta = chunk.choices[0].delta
            if delta.content:
                buffer += delta.content 
                if is_valid_markdown(buffer):
                    yield buffer 
                    buffer = ""                 

@app.post("/query-docs")
async def query(req:QueryDoc):
    chat = ChatDocs()
    res = chat(req.model_dump())
    return StreamingResponse(stream_processor(res), media_type="text/event-stream")

@app.post("/create-collection")
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
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_level="info", debug=True)