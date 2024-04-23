import os

from openai import OpenAI

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

    def chat_completion(self, chat_completion_request: ChatCompletionRequest):
        return self.client.chat.completions.create(
            **chat_completion_request.model_dump()
        )
