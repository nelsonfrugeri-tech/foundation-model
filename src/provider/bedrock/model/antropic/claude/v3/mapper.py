import json

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import (
    Usage,
    Message as MessageResponse,
    Prompt,
    TextResponse,
)

from provider.bedrock.model.antropic.claude.v3.request import *


class Claude3Mapper:

    @classmethod
    def serializer(cls, text_request_body: TextRequest) -> Claude3Request:
        return Claude3Request(
            messages=[
                Message(role=msg.role, content=[Content(type="text", text=msg.content)])
                for msg in text_request_body.prompt.messages
            ],
            temperature=text_request_body.prompt.parameter.temperature,
            max_tokens=text_request_body.prompt.parameter.maxTokens,
        )

    @classmethod
    def deserializer(cls, response: dict) -> TextResponse:
        result = json.loads(response.get("body").read())

        return TextResponse(
            usage=Usage(
                completionTokens=result["usage"]["input_tokens"],
                promptTokens=result["usage"]["output_tokens"],
                totalTokens=(
                    result["usage"]["input_tokens"] + result["usage"]["output_tokens"]
                ),
            ),
            prompt=Prompt(
                messages=[
                    MessageResponse(
                        role=result.get("role"),
                        content=result.get("content", [])[0]["text"],
                    )
                ]
            ),
        )
