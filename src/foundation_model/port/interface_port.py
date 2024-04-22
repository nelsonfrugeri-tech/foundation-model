from abc import ABC, abstractmethod

from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest


class InterfacePort(ABC):
    @abstractmethod
    def generate_text(self, text_request_body: TextRequest):
        pass
