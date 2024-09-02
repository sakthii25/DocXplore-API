from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class VectorType(str, Enum):
    DENSE = "dense"
    SPARSE = "sparse"

class TextType(str, Enum):
    INDEX = "index"
    SEARCH = "search"

class Vectors(BaseModel):
    vec_name : str
    type : VectorType
    value : List[float]|List[List[float]]

class Data(BaseModel):
    type : TextType
    id : str 
    text : str 
    metadata : dict = {}
    vectors : list[Vectors] = []

    