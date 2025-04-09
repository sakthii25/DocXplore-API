import os 

# Default collection and vector names
DEFAULT_SUMMARY_COLLECTION_NAME = "doc_summary"
DEFAULT_VECTOR_NAME = "text_dense_vec"

# Field keys
TEXT = "text"
CODE = "code"
CONTEXT = "context"
DOC_ID = "document_id"
CHUNK_ID = "chunk_id"
PARENT_ID = "parent_id"


# Prompt and response keys
PROMPT = "prompt"
SYSTEM_PROMPT = "system_prompt"
USER_PROMPT = "user_prompt"
RESPONSE = "response"

# env
AZURE_GPT_DEPLOYMENT_NAME = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")
AZURE_EMB_DEPLOYMENT_NAME = os.getenv("AZURE_EMB_DEPLOYMENT_NAME")
AZURE_BASE_URL = os.getenv("AZURE_OAI_BASE_URL") 
AZURE_API_VERSION = os.getenv("AZURE_OAI_API_VERSION")
AZURE_API_KEY = os.getenv("AZURE_OAI_API_KEY")
