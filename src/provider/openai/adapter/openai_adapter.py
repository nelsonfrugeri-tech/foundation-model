from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import *

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)
from provider.openai.service.openai_service import OpenAIService

from provider.port.interface_port import InterfacePort


class OpenAIAdapter(InterfacePort):

    def __init__(self):
        self.openai = OpenAIService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        response = self.openai.chat_completion(
            ChatCompletionRequest(
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
                completionTokens=response.usage.completion_tokens,
                promptTokens=response.usage.prompt_tokens,
                totalTokens=response.usage.total_tokens,
            ),
            prompt=Prompt(
                messages=[
                    Message(
                        role=response.choices[0].message.role,
                        content=response.choices[0].message.content,
                    )
                ]
            ),
        )
