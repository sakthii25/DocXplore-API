from flask import Flask, jsonify, request
from router.index.index_docs import IndexDocs 
from router.query.chat_docs import ChatDocs
from router.helper_functions import create_collections,delete_collections

app = Flask(__name__)

@app.get("/")
def root():
    return {"message" : "Hello World!"}

@app.get("/healthcheck")
def health_check():
    return {"response": "ok"}

@app.post("/index-docs")
def index():
    req = request.json
    index = IndexDocs()
    res = index(req)
    return jsonify(res)

@app.post("/query-docs")
def query():
    req = request.json
    chat = ChatDocs()
    res = chat(req)
    return jsonify(res)

@app.get("/create-collection")
def create_collection():
    req = request.json
    res = create_collections(req)
    return jsonify(res)

@app.get("/delete-collection")
def delete_collection():
    req = request.json
    res = delete_collections(req)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5215)