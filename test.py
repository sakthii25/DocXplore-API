# from router.index.index_docs import IndexDocs

# obj = IndexDocs()

# path = "/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt"
# path = "/Users/sakthi.n/Documents/Project/spyo/Archive0/102_hyper-checkout_android_base-sdk-integration_order-status-api.md"
# res = obj.index(path,collection_name='CLG')

# print(res)

# from router.query.chat_docs import ChatDocs 

# obj = ChatDocs() 

# res = obj.chat(query="Give me a sample request and response example for order status api",collection_name="CLG")
# print(res)

# print(res.metadata['prompt'])
# print(res.metadata['response'])
# To index
# curl 'http://127.0.0.1:5215/index-docs' -X POST -H 'Content-Type: application/json' --data-raw '{"path":"/Users/sakthi.n/Documents/clg/DocXplore-API/test.txt"}'


# from router.helper_functions import AtlasClient 

# uri = "mongodb+srv://sakthii25:#Sakpymango25@test.ddrmsow.mongodb.net/?retryWrites=true&w=majority&appName=Test"

# cli = AtlasClient(uri,'Test') 
# # print(cli.get_collection('API-KEY'))

# # print(cli.insert('API-KEY',{'key' : 123456789}))
# print(cli.insert('API-KEY',{'key' : "123456789"}))

# from core.llm import OpenRouterLLM 
# from data.types import Data,TextType


# q = Data(type=TextType.QUERY,content = "")

# q.metadata["system_prompt"] = "you are good ai"
# q.metadata["user_prompt"] = "tell me about rag system"

# llm = OpenRouterLLM(api_key="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")

# llm(q)

# print(q.metadata["response"])


# from sentence_transformers import SentenceTransformer

# # # Load the GTE model (large)
# model = SentenceTransformer("thenlper/gte-large")

# # Your query or text
# query = "query: What is the meaning of life?"

# # Get the embedding
# embedding = model.encode([query], normalize_embeddings=True)

# print("Embedding vector:", type(embedding[0]))
# print(len(embedding[0]))