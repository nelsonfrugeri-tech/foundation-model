import os

from anthropic import Anthropic

from foundation_model.antrhopic.adapter.model.request.message_request import (
    MessageRequest,
)


class AnthropicService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))

    def message(self, message_request: MessageRequest):
        return self.client.messages.create(**message_request.model_dump())
