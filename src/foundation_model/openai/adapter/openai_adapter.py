from foundation_model.port.interface_port import InterfacePort

from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest
from modelhub.api.adapter.http.v1.model.response.text_response import *

from foundation_model.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)

from foundation_model.openai.adapter.service.openai_service import OpenAIService


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
