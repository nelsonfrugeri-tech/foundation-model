
import json

from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest
from modelhub.api.adapter.http.v1.model.response.text_response import *

from modelhub.provider.openai.adapter.model.request.chat_completion_request import ChatCompletionRequest
from modelhub.provider.openai.adapter.service.openai_service import OpenAIService


class TextBusiness:

    def __init__(self):
        self.openai = OpenAIService()
    
    def generate(self, text_request_body: TextRequest):
        message_dicts = [msg.dict() for msg in text_request_body.prompt.messages]

        response = self.openai.chat_completion(
            ChatCompletionRequest(
                model=text_request_body.provider.model.name,
                messages=message_dicts
            )
        )

        return TextResponse(
            usage=Usage(
                completionTokens=response.usage.completion_tokens,
                promptTokens=response.usage.prompt_tokens,
                totalTokens=response.usage.total_tokens
            ),
            prompt=Prompt(
                messages=[Message(
                    role=response.choices[0].message.role, 
                    content=response.choices[0].message.content
                )]
            )
        )