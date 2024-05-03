from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.bedrock.port.bedrock_port import BedrockPort
from provider.bedrock.service.bedrock_service import BedrockService
from provider.bedrock.model.meta.llama.v3.llama3_mapper import Llama3Mapper


class Llama3Adapter(BedrockPort):
    def __init__(self):
        self.bedrock_service = BedrockService()

    def invoke_model(self, model: str, text_request_body: TextRequest) -> TextResponse:
        return Llama3Mapper.deserializer(
            self.bedrock_service.invoke_model(
                model=model,
                request_body=Llama3Mapper.serializer(text_request_body).model_dump(),
            )
        )
