from typing import List, Optional
from pydantic import BaseModel, Field

class ResponseContent(BaseModel):
    type: str = "text"
    text: str

class ResponseMessage(BaseModel):
    role: str
    content: List[ResponseContent]

class ResponsesRequest(BaseModel):
    model: str
    input: List[ResponseMessage]
    temperature: Optional[float] = None
    max_output_tokens: Optional[int] = Field(default=None, alias="max_tokens")

    def set_temperature(self, temperature: float) -> None:
        if temperature is not None:
            self.temperature = temperature

    def set_max_tokens(self, max_tokens: int) -> None:
        if max_tokens is not None:
            self.max_output_tokens = max_tokens
