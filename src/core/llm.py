from typing import Any
from openai import AzureOpenAI
from src.data.types import Data

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

    def chat_payload(self,sys_prompt,usr_query):
        sys = {
            'role' : 'system',
            'content' : sys_prompt
        }
        usr = {
            'role' : 'user',
            'content' : usr_query
        }
        chat_payload = {
            'messages' : [sys,usr],
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
        sys_prompt = query.metadata['prompt']
        usr_query = query.content 

        chat_payload = self.chat_payload(sys_prompt,usr_query)

        res = self.call_llm(chat_payload)

        query.metadata['response'] = res
        return query

    def __call__(self, query:Data):
        return self.chat(query)



