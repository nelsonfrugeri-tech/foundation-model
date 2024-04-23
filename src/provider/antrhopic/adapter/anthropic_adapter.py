from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import *

from provider.port.interface_port import InterfacePort

from provider.antrhopic.service.anthropic_service import AnthropicService
from provider.antrhopic.adapter.model.request.message_request import (
    MessageRequest,
)


class AnthropicAdapter(InterfacePort):
    def __init__(self):
        self.anthropic = AnthropicService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        response = self.anthropic.message(
            MessageRequest(
                model=text_request_body.provider.model.name,
                messages=[
                    msg.model_dump() for msg in text_request_body.prompt.messages
                ],
                temperature=text_request_body.prompt.parameter.temperature,
                max_tokens=text_request_body.prompt.parameter.maxTokens,
            )
        )

        return TextResponse(
            usage=Usage(
                completionTokens=response.usage.output_tokens,
                promptTokens=response.usage.input_tokens,
                totalTokens=(
                    response.usage.input_tokens + response.usage.output_tokens
                ),
            ),
            prompt=Prompt(
                messages=[
                    Message(
                        role="assistant",
                        content=response.content,
                    )
                ]
            ),
        )
