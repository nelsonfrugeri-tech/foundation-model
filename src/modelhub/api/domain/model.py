from pydantic import BaseModel

from typing import Optional, Field


class Parameter(BaseModel):
    temperature: Optional[float]
    maxTokens: Optional[int] = Field(..., alias="max_tokens")


class Model(BaseModel):
    id: int
    name: str
    description: str
    label: str
    parameter: Optional[Parameter]
