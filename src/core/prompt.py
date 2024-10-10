from typing import Any
from src.core.vectordb import QdrantDB

from src.data.types import Data

default_prompt="""
You are a highly intelligent and precise question-answering assistant.
Your task is to provide an accurate and concise answer based solely on the given document summary.

Doc Summary:
{DOC_SUMMARY}

Instructions:
The Doc Summary section provides a summary of the most relevant summaries of the document related to the user question.
Use these sections to answer the User Question.
"""

code_prompt = """
You are a highly intelligent and precise coding assistant bot.
Your task is to provide an accurate and concise code part based on the document code examples.

Prev LLM response:
{CONTEXT}

Code examples:
{CODE}

Instructions:
Prev LLM response is used to provide the holistic understanding of the question 
code examples contain the some static setup code snippets.Sometimes it is None so there is no code snippets 
Use these prev llm response and code snippets to answer the User Question with code example if its needed or relavent.
Ask follow-up questions if additional context or clarification is needed.
"""

summarizer_prompt="""
You are a very good document summarizer
Your task is to summarize the whole document without losing any vital information.

Document
{DOCUMENT}

Instructions:
summarize the document so that anyone can able to understand the over all meaning without looking  into actual document
"""

codextractor_prompt = """
You are a code extractor 
Your task is to extract the code part from the document if it have any code content in it

Document
{DOCUMENT}

Instructions:
Extract the code content from document.If no code part in the document respond None otherwise give the code part
"""

class PromptBase:
    def __init__(self) -> None:
        pass

    def generate_prompt(self,query:Data):
        raise NotImplementedError

    def __call__(self, query:Data):
        return self.generate_prompt(query)
class AugmentPrompt(PromptBase):

    def __init__(self) -> None:
      super().__init__()
      self.prompt = default_prompt
      pass

    def generate_prompt(self,query:Data):

        try:
            context = query.metadata['context']
        except:
            raise Exception("There is no retrived context in Data")
        
        summary = ""
        db = QdrantDB()
        mp = [] 

        for context in context:
            id = context['parent_id']

            if not id in mp:
                res = db.search_point('doc summary',id)
                summary += res.payload['text'] + "\n"
                mp.append(id)

        prompt = self.prompt.format(DOC_SUMMARY=summary)
        query.metadata['prompt'] = prompt

        return query
class CodePrompt(PromptBase):
    def __init__(self) -> None:
        super().__init__()
        self.prompt = code_prompt
        pass

    def generate_prompt(self, query: Data):
        try:
            prev_response = query.metadata['response']
        except:
            raise Exception("There is no response from the previous llm call") 
        
        context = query.metadata['context']
        
        code_snippets = ""
        db = QdrantDB()
        mp = [] 

        for context in context:
            id = context['parent_id']

            if not id in mp:
                res = db.search_point('doc summary',id)
                code_snippets += res.payload['code'] + "\n"
                mp.append(id)
        
        prompt = self.prompt.format(CONTEXT=prev_response,CODE=code_snippets)
        query.metadata['prompt'] = prompt
        return query

class SummarizerPrompt(PromptBase):
    def __init__(self) -> None:
        super().__init__()
        self.prompt = summarizer_prompt
        pass


    def generate_prompt(self,query:Data):

        content = query.content
        query.metadata['prompt'] = self.prompt.format(DOCUMENT=content)

        return query

class CodextractorPrompt(PromptBase):

    def __init__(self) -> None:
        super().__init__()
        self.prompt = codextractor_prompt
        pass 

    def generate_prompt(self,query:Data):
        
        content  = query.content 
        query.metadata['prompt'] = self.prompt.format(DOCUMENT=content)

        return query


