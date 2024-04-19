from pydantic import BaseModel
from typing import List, Optional

class Usage(BaseModel):
    completionTokens: int
    promptTokens: int
    totalTokens: int

class Message(BaseModel):
    role: str
    content: str

class Prompt(BaseModel):
    messages: List[Message]

class TextResponse(BaseModel):
    usage: Usage
    prompt: Prompt