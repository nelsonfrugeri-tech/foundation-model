from pydantic import BaseModel

from hub.api.domain.model import Model


class Provider(BaseModel):
    id: int
    name: str
    description: str
    label: str
    model: Model
