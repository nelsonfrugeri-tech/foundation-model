import json

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import (    
    Message,
    Prompt,
    TextResponse
)

from provider.bedrock.model.meta.llama.v3.llama3_request import *
from provider.bedrock.model.meta.llama.v3.llama3_prompt import Llama3Prompt

class Llama3Mapper:

    @classmethod
    def serializer(cls, text_request: TextRequest) -> Llama3Request:
        prompt = (
            Llama3Prompt.function_calling(
                messages=text_request.prompt.messages,
                tools=text_request.tools
            )
                if text_request.tools is not None and len(text_request.tools) > 0 
                else Llama3Prompt.completion(
                    messages=text_request.prompt.messages
                )
        )

        return Llama3Request(
            prompt=prompt,
            max_gen_len=text_request.prompt.parameter.maxTokens,
            temperature=text_request.prompt.parameter.temperature,            
        )
    
    @classmethod
    def deserializer(cls, response: dict) -> TextResponse:
        result = json.loads(response["body"].read())

        return TextResponse(
            prompt=Prompt(
                messages=[
                    Message(
                        role="assistant",
                        content=str(result["generation"]),
                    )
                ]
            ),
        )