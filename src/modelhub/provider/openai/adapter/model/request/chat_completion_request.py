from pydantic import BaseModel, validator
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[List[str]] = None

    @validator('temperature', 'top_p')
    def check_probability(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Probability values must be between 0 and 1')
        return v