import json

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.port.interface_port import InterfacePort

from provider.bedrock.service.bedrock_service import BedrockService
from provider.bedrock.provider.antropic.mapper.claude_3_mapper import Claude3Mapper


class BedrockAdapter(InterfacePort):
    def __init__(self):
        self.bedrock = BedrockService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        return Claude3Mapper.deserializer(
            self.bedrock.invoke_model(            
                model=text_request_body.provider.model.name,
                body_request=Claude3Mapper.serializer(text_request_body)
            )
        )
