from pydantic import BaseModel, Field
from typing import List, Dict

class ProviderModel(BaseModel):
    name: str

class Provider(BaseModel):
    name: str
    model: ProviderModel

class PromptParameter(BaseModel):
    temperature: float
    maxTokens: int = Field(..., alias='max_tokens')

class Message(BaseModel):
    role: str
    content: str

class Prompt(BaseModel):
    parameter: PromptParameter
    messages: List[Message]

class ToolParameter(BaseModel):
    type: str
    properties: Dict

class Tool(BaseModel):
    name: str
    description: str
    parameters: ToolParameter

class TextRequest(BaseModel):
    provider: Provider
    prompt: Prompt
    tools: List[Tool]