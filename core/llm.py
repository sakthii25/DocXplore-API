from openai import AzureOpenAI

import requests
from data.types import Data,Message
from core.constants import *

class AzureGPTLLM():
    def __init__(self, deployment_name=None, api_base=None, api_version=None, api_key=None, stream=False, max_tokens=1000) -> None:
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.api_version = api_version
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.stream = stream

        self.client = AzureOpenAI(
            azure_endpoint=self.api_base,
            azure_deployment=self.deployment_name,
            api_version=self.api_version,
            api_key=self.api_key
        )

        self.default_gen_config = {
            "max_tokens": 4000,
            "temperature": 0.01,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 0.95,
            "stop": None
        }

    def chat_payload(self, sys_prompt, usr_query):

        sys = Message(role = "system", content = sys_prompt)
        usr = Message(role = "user", content = usr_query)
 
        chat_payload = {
            'messages' : [sys.dict(),usr.dict()],
            **self.default_gen_config
        }
        return chat_payload
    
    def call_llm(self,chat_payload):
        response = self.client.chat.completions.create(
                **chat_payload,
                model=self.deployment_name,
                stream=self.stream,
            )
        response =  response.choices[0].message.content
        return response
    
    def chat(self,query:Data):
        sys_prompt = query.metadata[SYSTEM_PROMPT]
        usr_query = query.metadata[USER_PROMPT]

        chat_payload = self.chat_payload(sys_prompt,usr_query)

        res = self.call_llm(chat_payload)

        query.metadata[RESPONSE] = res
        return query

    def __call__(self, query:Data):
        return self.chat(query)
    
class OpenRouterLLM():
    def __init__(self, api_key = None, model = "google/gemini-flash-1.5-8b-exp", stream = False) -> None:
        
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization" : f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.payload = {
           "model": model
        }
        self.stream = stream
        pass 

    def chat_payload(self, sys_prompt, usr_query):

        sys = Message(role = "system", content = sys_prompt)
        usr = Message(role = "user", content = usr_query)

        self.payload["messages"] = [sys.dict(),usr.dict()]

        return self.payload
     
    def call_llm(self,chat_payload):

        response = requests.post(url=self.url, json=chat_payload, headers=self.headers).json()
        return  response["choices"][0]["message"]["content"]
    
    def chat(self,query:Data):
        sys_prompt = query.metadata[SYSTEM_PROMPT]
        usr_query = query.metadata[USER_PROMPT]

        chat_payload = self.chat_payload(sys_prompt,usr_query)

        res = self.call_llm(chat_payload)

        query.metadata[RESPONSE] = res
        return query

    def __call__(self, query:Data):
        return self.chat(query)