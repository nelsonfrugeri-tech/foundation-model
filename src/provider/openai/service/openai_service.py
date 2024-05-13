import os

from dotenv import load_dotenv

from openai import OpenAI

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)


class OpenAIService:
    def __init__(self):
        load_dotenv()
        
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat_completion(self, chat_completion_request: ChatCompletionRequest):
        return self.client.chat.completions.create(
            **chat_completion_request.model_dump()
        )
