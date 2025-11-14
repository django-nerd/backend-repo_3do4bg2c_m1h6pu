from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

# Define collections via Pydantic models (class name lowercased => collection)

class Message(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=200)
    phone: Optional[str] = Field(None, max_length=30)
    subject: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=5, max_length=5000)

class Project(BaseModel):
    title: str
    stack: List[str]
    description: str
    code_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None
    cover: Optional[str] = None
