from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.bedrock.port.bedrock_port import BedrockPort
from provider.bedrock.model.antropic.claude.v3.service import Claude3Service
from provider.bedrock.model.antropic.claude.v3.mapper import Claude3Mapper


class Claude3Adpter(BedrockPort):
    def __init__(self):
        self.claude3_service = Claude3Service()

    def invoke_model(self, model: str, text_request_body: TextRequest) -> TextResponse:
        return Claude3Mapper.deserializer(
            self.claude3_service.invoke_model(
                model=model,
                request_body=Claude3Mapper.serializer(text_request_body),
            )
        )
