from pydantic import BaseModel


class Llama3Request(BaseModel):
    prompt: str
    max_gen_len: int = 512
    temperature: float = 0.0
    top_p: float = 1.0
