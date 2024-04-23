from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest

from foundation_model.provider.openai.adapter.openai_adapter import OpenAIAdapter
from foundation_model.provider.antrhopic.adapter.anthropic_adapter import AnthropicAdapter
from foundation_model.provider.bedrock.adapter.bedrock_adapter import BedrockAdapter
from foundation_model.port.interface_port import InterfacePort


class ProviderService:
    def __init__(self):
        self.providers = {
            "openai": OpenAIAdapter(),
            "anthropic": AnthropicAdapter(),
            "bedrock": BedrockAdapter(),
        }

    def generate_text(
        self, provider_name: str, text_request_body: TextRequest
    ) -> InterfacePort:
        return self.providers[provider_name].generate_text(text_request_body)