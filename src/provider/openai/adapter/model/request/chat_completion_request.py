from pydantic import BaseModel, field_validator
from typing import List, Optional

from modelhub.api.adapter.http.v1.model.exception.bad_request_exception import (
    BadRequestException,
)


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

    @field_validator("temperature", "top_p")
    def check_probability(cls, value, ctx):
        if value is not None and (value < 0.0 or value > 1.0):
            raise BadRequestException(
                params=[f"The {ctx.field_name} field must be between 0 and 1"]
            )
        return value
