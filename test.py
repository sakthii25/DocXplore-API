# from router.index.index_docs import IndexDocs

# obj = IndexDocs()

# path = "/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt"
# path = "/Users/sakthi.n/Documents/Project/spyo/Archive0/4_hyper-checkout_android_base-sdk-integration_getting-sdk.md"
# res = obj.index(path,collection_name='CLG')

# print(res)

from router.query.chat_docs import ChatDocs 

obj = ChatDocs() 

res = obj.chat(query="how to get the hyperchekout SDK in java",collection_name="CLG")
print(res)

# print(res.metadata['prompt'])
# print(res.metadata['response'])
# To index
# curl 'http://127.0.0.1:5215/index-docs' -X POST -H 'Content-Type: application/json' --data-raw '{"path":"/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt"}'

