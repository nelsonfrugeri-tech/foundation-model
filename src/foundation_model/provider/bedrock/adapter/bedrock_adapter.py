import json

from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest
from modelhub.api.adapter.http.v1.model.response.text_response import *

from foundation_model.port.interface_port import InterfacePort

from foundation_model.provider.bedrock.service.bedrock_service import BedrockService
from foundation_model.provider.bedrock.adapter.model.request.body_request import *


class BedrockAdapter(InterfacePort):
    def __init__(self):
        self.bedrock = BedrockService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        response = self.bedrock.invoke_model(
            model=text_request_body.provider.model.name,
            body_request=BodyRequest(
                messages=[
                    Message(
                        role=msg.role, content=Content(type="text", text=msg.content)
                    )
                    for msg in text_request_body.prompt.messages
                ],
                temperature=text_request_body.prompt.parameter.temperature,
                max_tokens=text_request_body.prompt.parameter.maxTokens,
            ),
        )

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
                    Message(
                        role=result.get("role"),
                        content=result.get("content", []),
                    )
                ]
            ),
        )
