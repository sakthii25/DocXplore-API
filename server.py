from flask import Flask, jsonify, request

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
    return {"message" : "indexing"}

@app.post("/query-docs")
def query_docs():
    req = request.json
    print(req)
    return {"message" : "quering"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5215)