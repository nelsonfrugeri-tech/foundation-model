from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ProviderModel(BaseModel):
    name: str


class Provider(BaseModel):
    name: str
    model: ProviderModel


class PromptParameter(BaseModel):
    temperature: Optional[float] = None
    maxTokens: Optional[int] = Field(None, alias="max_tokens")


class Message(BaseModel):
    role: str
    content: str


class Prompt(BaseModel):
    parameter: Optional[PromptParameter] = None
    messages: List[Message]


class Properties(BaseModel):
    type: str
    description: Optional[str] = None
    enum: Optional[list] = None


class ToolParameter(BaseModel):
    type: str
    properties: Dict[str, Properties]
    required: Optional[List[str]] = None


class Tool(BaseModel):
    name: str
    description: str
    parameters: Optional[ToolParameter]


class TextRequest(BaseModel):
    provider: Provider
    prompt: Prompt
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[str] = None
