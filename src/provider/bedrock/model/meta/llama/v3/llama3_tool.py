from pydantic import BaseModel
from typing import List, Optional


class Properties(BaseModel):
    name: str # That's the tool name
    parameters: Optional[dict] # These are the parameters of the tool, only fill them in if you have a reference to the input parameters


class Tool(BaseModel):
    properties: Properties


class Tools(BaseModel):
    tools: List[Tool]