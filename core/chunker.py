from typing import Any
from data.types import Data,TextType
import uuid

class Chunking():
    def __init__(self, chunk_size=1000, overlap=200, min_chunk_len=5, split_func=None) -> None:
        """ split text into chunk of words of with given chunk size length, llm token size is ignored.

            Inspired by LangChain's recursive text splitter
        """
        self.chunk_size = chunk_size 
        
        if chunk_size <= overlap:
            raise f"Chunksize can not be less than or equal to overlap, chunksize: {chunk_size}, overlap: {overlap}"
        
        if chunk_size < min_chunk_len:
            raise f"Chunksize can not be less than min_chunk_len, chunksize: {chunk_size}, min_chunk_len: {min_chunk_len}"

        self.min_chunk_len = min_chunk_len
        self.overlap = overlap
        self.split_func = split_func or (lambda x : x.split(" "))


    def create_chunkID(self):
        id = uuid.uuid4().hex
        return id
    
    def chunk_text(self, document:Data):
        """ split long text to chunk of text with given chunk size

            words will be split based on split func

            heading is ignored in basic chunking
        """
        type = document.type 
        content = document.content
        metadata = document.metadata
        id = document.id
        chunks = []

        def add_overlap_to_context(chunk, overlap):
            return  " ".join(overlap) + " " + " ".join(chunk) 
        
        def add_chunk(curr_chunk, overlap_chunk):
            if len(curr_chunk) + self.overlap > self.min_chunk_len:
                chunk_text = add_overlap_to_context(curr_chunk, overlap_chunk)
                metadata["chunk_id"] = self.create_chunkID()
                chunk = Data(type = type,content = chunk_text,id = id,metadata = metadata)
                chunks.append(chunk)

        curr_chunk = []
        overlap_chunk = []
        
        for word in self.split_func(content):
            if len(curr_chunk) + self.overlap < self.chunk_size:
                curr_chunk.append(word)
            else:
                add_chunk(curr_chunk, overlap_chunk)
                overlap_chunk = curr_chunk[-self.overlap:]
                curr_chunk = []

        add_chunk(curr_chunk, overlap_chunk)
        return chunks   
    
    def __call__(self, document):
        return self.chunk_text(document)