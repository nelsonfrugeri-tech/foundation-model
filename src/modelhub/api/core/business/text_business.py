from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest
from modelhub.api.adapter.http.v1.model.response.text_response import *
from foundation_model.provider import ProviderHub


class TextBusiness:

    def __init__(self):
        self.provider_hub = ProviderHub()

    def generate(self, text_request_body: TextRequest):
        return self.provider_hub.generate_text(
            provider_name=text_request_body.provider.name,
            text_request_body=text_request_body,
        )
