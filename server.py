from flask import Flask, jsonify, request
from router.index import index_docs 
from router.query import chat_docs
from router.helper import create_collection

app = Flask(__name__)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/healthcheck")
def health_check():
    return {"response": "ok"}

@app.post("/index-docs")
def index_docs():
    req = request.json
    res = index_docs(req)
    return jsonify(res)

@app.post("/query-docs")
def query_docs():
    req = request.json
    res = chat_docs(req)
    return res

@app.get("/create-collection")
def create_collection():
    req = request.json
    res = create_collection(req)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5215)