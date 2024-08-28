from index.index_docs import IndexDocs 

obj = IndexDocs()

res = obj.index("/Users/sakthi.n/Documents/clg/test.txt")

print(len(res))