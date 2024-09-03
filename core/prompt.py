from core.vectordb import QdrantDB

from data.types import Data

default_prompt="""
You are a highly intelligent and precise question-answering assistant.
Your task is to provide an accurate and concise answer based solely on the given document summary.

Doc Summary:
{DOC_SUMMARY}

Instructions:
The Doc Summary section provides a summary of the most relevant summaries of the document related to the user question.
Use these sections to answer the User Question.
"""

summarizer_prompt="""
        You are a very good document summarizer
        Your task is to summarize the whole document without losing any vital information.

        Document
        {DOCUMENT}

        Instructions:
        summarize the document so that anyone can able to understand the over all meaning without looking  into actual document
    """

class AugmentPrompt:

    def __init__(self) -> None:
        self.prompt = default_prompt
        pass


    def generate_prompt(self,query:Data):

        try:
            context = query.metadata['context']
        except:
            raise Exception("There is no context in Data")
        
        summary = ""
        db = QdrantDB()
        mp = [] 

        for context in context:
            id = context['parent_id']

            if not id in mp:
                res = db.search_point('doc summary',id)
                summary += res.payload['text']
                mp.append(id)

        prompt = self.prompt.format(DOC_SUMMARY=summary)
        query.metadata['prompt'] = prompt

        return query


    def __call__(self, query:Data):
        return self.generate_prompt(query)
    
class SummarizerPrompt:
    def __init__(self) -> None:
        self.prompt = summarizer_prompt
        pass


    def generate_prompt(self,query:Data):

        content = query.content
        query.metadata['prompt'] = self.prompt.format(DOCUMENT=content)

        return query


    def __call__(self, query:Data):
        return self.generate_prompt(query)

