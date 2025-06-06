from hub.api.adapter.http.v1.model.request.text_request import TextRequest

from provider.openai.adapter.openai_adapter import OpenAIAdapter
from provider.antrhopic.adapter.anthropic_adapter import AnthropicAdapter
from provider.bedrock.adapter.bedrock_adapter import BedrockAdapter
from provider.gemini.adapter.gemini_adapter import GeminiAdapter
from provider.port.interface_port import InterfacePort


class ProviderService:
    def __init__(self):
        self.providers = {
            "openai": OpenAIAdapter(),
            "gemini": GeminiAdapter(),
        }

    def generate_text(
        self, provider_name: str, text_request_body: TextRequest
    ) -> InterfacePort:
        return self.providers[provider_name].generate_text(text_request_body)
