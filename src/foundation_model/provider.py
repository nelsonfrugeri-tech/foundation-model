from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest

from foundation_model.openai.adapter.openai_adapter import OpenAIAdapter
from foundation_model.antrhopic.adapter.anthropic_adapter import AnthropicAdapter
from foundation_model.bedrock.adapter.bedrock_adapter import BedrockAdapter


class ProviderHub:
    def __init__(self):
        self.providers = {
            "openai": OpenAIAdapter(),
            "anthropic": AnthropicAdapter(),
            "bedrock": BedrockAdapter(),
        }

    def generate_text(self, provider_name: str, text_request_body: TextRequest):
        return self.providers[provider_name].generate_text(text_request_body)
