import os

from dotenv import load_dotenv

from openai import OpenAI

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)

from observerai.openai import metric_chat_create

class OpenAIService:
    def __init__(self):
        load_dotenv()        
        self.client = OpenAI()

    @metric_chat_create()
    def chat_completion(self, chat_completion_request: ChatCompletionRequest):
        return self.client.chat.completions.create(
            **chat_completion_request.model_dump()
        )
