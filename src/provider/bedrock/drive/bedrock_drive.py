from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.bedrock.model.antropic.claude.v3.adapter import Claude3Adpter
from provider.bedrock.model.meta.llama.v3.llama3_adapter import Llama3Adapter


class BedrockDrive:
    def __init__(self):
        self.models = {
            "anthropic.claude-3-sonnet-20240229-v1:0": Claude3Adpter(),
            "meta.llama3-70b-instruct-v1:0": Llama3Adapter(),
        }

    def invoke_model(self, model: str, text_request_body: TextRequest) -> TextResponse:
        return self.models[model].invoke_model(
            model=text_request_body.provider.model.name,
            text_request_body=text_request_body,
        )
