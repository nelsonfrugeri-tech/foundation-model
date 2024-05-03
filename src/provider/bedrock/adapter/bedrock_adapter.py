import json

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.port.interface_port import InterfacePort

from provider.bedrock.model.antropic.claude.v3.mapper import Claude3Mapper

from provider.bedrock.drive.bedrock_drive import BedrockDrive


class BedrockAdapter(InterfacePort):
    def __init__(self):
        self.bedrock_drive = BedrockDrive()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        return self.bedrock_drive.invoke_model(
            model=text_request_body.provider.model.name,
            text_request_body=text_request_body,
        )
