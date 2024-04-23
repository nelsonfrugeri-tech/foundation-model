from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class MessageRequest(BaseModel):
    model: str
    messages: List[Message] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None