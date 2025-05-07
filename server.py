
import json
import uuid
import logging
import uvicorn

from datetime import datetime, timezone
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from router.index.index_docs import IndexDocs 
from router.query.chat_docs import ChatDocs
from router.helper_functions import *
from data.psql import Postgres
from data.queries import * 
from data.types import *
import markdown

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

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

GOOGLE_CLIENT_ID = "624900351596-f8vdqicse3q2vh3stk01p9h5fo9fdp3b.apps.googleusercontent.com"

class GoogleToken(BaseModel):
    token: str 

@app.post("/auth/google")
async def google_auth(payload: GoogleToken):
    try:
        psql = Postgres()
        id_info = id_token.verify_oauth2_token(
            payload.token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
        email = id_info.get("email")
        name = id_info.get("name")
        last_login = datetime.now(timezone.utc)
        
        if (psql.select_query(SELECT_USER_QUERY,(email,)) != []):
            print("Updating a user")
            psql.update_query(UPDATE_USER_QUERY,(last_login, email))
        else:
            print("Creating a user")
            user_id = uuid.uuid5(uuid.NAMESPACE_DNS, email)
            psql.insert_query(INSERT_USER_QUERY, (user_id, name, email, last_login))

        psql.close()
        return JSONResponse(content={
            "email": email,
            "name": name,
            "status": "authenticated"
        })

    except Exception as e:
        print(f"OAuth verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

COLUMN_NAMES = ["id", "user_id", "document_name", "document_size", "uploaded_time"]

def serialize_row(row: tuple) -> dict:
    data = dict(zip(COLUMN_NAMES, row))
    data["uploaded_time"] = str(data["uploaded_time"])
    data["user_id"] = str(data["user_id"])
    data["id"] = str(data["id"])
    return data

@app.post("/list-documents")
def get_documents(req: User):
    psql = Postgres()
    res = psql.select_query(SELECT_USER_QUERY,(req.user_email,))
    user_id = res[0][0]
    rows = psql.select_query(SELECT_QUERY, (user_id,))
    psql.close()
    sorted_rows = sorted(rows, key=lambda row: row[3], reverse=True)
    result = [serialize_row(row) for row in sorted_rows]
    return JSONResponse(content={"result": result})

@app.post("/list-collections") 
def get_collections(req: User):
    psql = Postgres()  
    res = psql.select_query(SELECT_USER_QUERY,(req.user_email,))
    user_id = res[0][0]
    row = psql.select_query(SELECT_COLLECTION_QUERY,(user_id,))
    if row == []:
        return JSONResponse(content={"collectionName": "", "summaryCollectionName": "", "isCreated": False})
    
    print(row)
    return JSONResponse(content={"collectionName": row[0][2], "summaryCollectionName": row[0][3], "isCreated": True})


@app.post("/list-apikeys")
def get_apikeys(req: User):
    psql = Postgres()  
    res = psql.select_query(SELECT_USER_QUERY,(req.user_email,))
    user_id = res[0][0]
    rows = psql.select_query(SELECT_API_KEY_QUERY,(user_id,))
    keys = dict() 
    keys["api_keys"] = []
    for row in rows:
        keys["api_keys"].append({"key" : row[0], "createdAt" : row[2]})
    
    return JSONResponse(content=keys)

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
        "uploaded_time": datetime.now(timezone.utc)
    }
    index = IndexDocs()
    result = index(json_data)
    result["uploaded_time"] = str(result["uploaded_time"])
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

@app.post("/add-apikey")
def add_apikey(req: ApiKey):
    psql = Postgres()
    res = psql.select_query(SELECT_USER_QUERY,(req.user_email,))
    user_id = res[0][0] 

    psql.insert_query(INSERT_API_KEY_QUERY,(req.api_key, user_id, req.created_at))
    psql.close()

    return JSONResponse({"response": "Api Key was created successfully"})

@app.post("/delete-apikey")
def delete_apikey(req: ApiKey):
    psql = Postgres()
    psql.delete_query(DELETE_API_KEY_QUERY,(req.api_key,))
    psql.close()
    return JSONResponse({"response": "Api Key was deleted successfully"})

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