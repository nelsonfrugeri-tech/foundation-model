import os

from dotenv import load_dotenv

from openai import OpenAI

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
)
from provider.openai.adapter.model.request.responses_request import (
    ResponsesRequest,
)

try:
    from observerai.openai import metric_chat_create
except Exception:  # pragma: no cover - observerai optional
    def metric_chat_create():  # type: ignore
        def decorator(func):
            return func

        return decorator


class OpenAIService:
    def __init__(self):
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_KEY"):
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
        self.client = OpenAI()

    @metric_chat_create()
    def chat_completion(self, chat_completion_request: ChatCompletionRequest):
        return self.client.chat.completions.create(
            **chat_completion_request.model_dump()
        )

    def responses(self, responses_request: ResponsesRequest):
        if not os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_KEY"):
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
        return self.client.responses.create(
            **responses_request.model_dump(),
        )
