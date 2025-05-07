from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# server types
class IndexDoc(BaseModel):
    path: str 
    collection_name: str 
    summary_collection_name: Optional[str] = None

class QueryDoc(BaseModel):
    query: str 
    user_email: Optional[str] = None
    # collection_name: str 
    # summary_collection_name: Optional[str] = None

class Collection(BaseModel):
    user_email: str
    collection_name: str 
    vector_name: Optional[str] = None
    summary_collection_name: Optional[str] = None

class Document(BaseModel):
    id: str 
    collection_name: str 
    summary_collection_name: str

class User(BaseModel):
    user_email: str

class ApiKey(BaseModel):
    user_email: str 
    api_key: str 
    created_at: Optional[str] = None

# internal types
class VectorType(str, Enum):
    DENSE = "dense"
    SPARSE = "sparse"

class TextType(str, Enum):
    INDEX = "index"
    QUERY = "query"

class Vectors(BaseModel):
    vec_name : str
    type : VectorType
    value : List[float] | List[List[float]]

class Data(BaseModel):
    type : TextType
    id : str = None
    parent : Optional[bool] = False
    content : str 
    metadata : dict = {}
    persist_to_db :list[str] = []
    vectors : list[Vectors] = []

class Message(BaseModel):
    role : str 
    content : str