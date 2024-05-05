from pydantic import BaseModel
from typing import List, Optional, Dict


class Usage(BaseModel):
    completionTokens: int
    promptTokens: int
    totalTokens: int


class Message(BaseModel):
    role: str
    content: Optional[str] = None


class Prompt(BaseModel):
    messages: List[Message]


class Tool(BaseModel):
    name: str
    arguments: dict


class TextResponse(BaseModel):
    usage: Optional[Usage] = None
    prompt: Prompt
    tools: Optional[List[Tool]] = None
