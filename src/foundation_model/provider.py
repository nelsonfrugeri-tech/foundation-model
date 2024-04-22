from foundation_model.openai.adapter.openai_adapter import OpenAIAdapter
from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest


class ProviderHub:
    def __init__(self):
        self.providers = {
            "openai": OpenAIAdapter(),
        }

    def generate_text(self, provider_name: str, text_request_body: TextRequest):
        return self.providers[provider_name].generate_text(text_request_body)
