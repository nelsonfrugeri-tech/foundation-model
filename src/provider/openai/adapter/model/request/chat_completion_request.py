from pydantic import BaseModel, field_validator, Field
from typing import List, Optional, Dict

from hub.api.adapter.http.v1.model.exception.bad_request_exception import (
    BadRequestException,
)


class Message(BaseModel):
    role: str
    content: str


class Properties(BaseModel):
    type: str
    description: Optional[str] = None
    enum: Optional[List[str]] = Field(default_factory=list)


class Parameters(BaseModel):
    type: str
    properties: Dict[str, Properties]
    required: Optional[List[str]] = Field(default_factory=list)

    # @field_validator('properties')
    # def check_required_properties(cls, properties, values):
    #     if 'required' in values:
    #         required_fields = values['required']
    #         for field in required_fields:
    #             if field not in properties:
    #                 raise ValueError(f"The field '{field}' is required but not defined in properties.")
    #     return properties


class Function(BaseModel):
    name: str
    description: str
    parameters: Optional[Parameters] = None


class Tool(BaseModel):
    type: str = 'function'
    function: Function 


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[str] = None

    @field_validator("temperature", "top_p")
    def check_probability(cls, value, ctx):
        if value is not None and (value < 0.0 or value > 1.0):
            raise BadRequestException(
                params=[f"The {ctx.field_name} field must be between 0 and 1"]
            )
        return value
    
    def set_temperature(self, temperature:float) -> None:
        if temperature is not None:
            self.temperature = temperature

    def set_max_tokens(self, max_tokens:int) -> None:
        if max_tokens is not None:
            self.max_tokens = max_tokens

    def set_tools(self, tools:List[Tool], tool_choice:str) -> None:
        if len(tools) > 0:
            self.tools = tools
            
            self.tool_choice = (
                tool_choice 
                if tool_choice is not None 
                else "auto"
            )
