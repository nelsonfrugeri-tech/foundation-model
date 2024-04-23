from pydantic import BaseModel
from typing import List, Optional


class Content(BaseModel):
    type: str
    text:str


class Message(BaseModel):
    role: str
    content: Content


class BodyRequest(BaseModel):
    messages: List[Message] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
