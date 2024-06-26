from abc import ABC, abstractmethod

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse


class InterfacePort(ABC):
    @abstractmethod
    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        pass
