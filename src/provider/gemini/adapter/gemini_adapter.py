from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import TextResponse

from provider.port.interface_port import InterfacePort
from provider.gemini.service.gemini_service import GeminiService
from provider.gemini.model import mapper


class GeminiAdapter(InterfacePort):
    def __init__(self):
        self.gemini = GeminiService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        messages, generation_config, tools = mapper.serialize_request(text_request_body)
        response = self.gemini.generate(
            model=text_request_body.provider.model.name,
            messages=messages,
            generation_config=generation_config,
            tools=tools,
            tool_choice=text_request_body.tool_choice or "auto",
        )
        return mapper.deserialize_response(response)
