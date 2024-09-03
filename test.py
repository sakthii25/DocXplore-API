# from router.index.index_docs import IndexDocs

# obj = IndexDocs()

# res = obj.index("/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt",collection_name='CLG')

# print(res)

from router.query.chat_docs import ChatDocs 

obj = ChatDocs() 

res = obj.chat(query="what is neural network? ",collection_name="CLG")

print(res.metadata['prompt'])
print(res.metadata['response'])
# To index
# curl 'http://127.0.0.1:5215/index-docs' -X POST -H 'Content-Type: application/json' --data-raw '{"path":"/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt"}'

