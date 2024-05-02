from pydantic import BaseModel
from typing import List, Optional


class Content(BaseModel):
    type: str
    text: str


class Message(BaseModel):
    role: str
    content: List[Content]


class Claude3Request(BaseModel):
    anthropic_version: str = "bedrock-2023-05-31"
    messages: List[Message] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
