import sys
import os
import types
sys.path.insert(0, os.path.abspath('src'))

# Mock observerai.openai.metric_chat_create decorator
observerai = types.ModuleType("observerai")
openai_mod = types.ModuleType("observerai.openai")
def metric_chat_create():
    def decorator(func):
        return func
    return decorator
openai_mod.metric_chat_create = metric_chat_create
observerai.openai = openai_mod
sys.modules["observerai"] = observerai
sys.modules["observerai.openai"] = openai_mod

from provider.openai.adapter.openai_adapter import OpenAIAdapter
from provider.openai.service.openai_service import OpenAIService
from hub.api.adapter.http.v1.model.request.text_request import (
    TextRequest,
    Provider,
    ProviderModel,
    Prompt,
    PromptParameter,
    Message,
)

def test_generate_text_chat_completion(monkeypatch):
    def dummy_init(self):
        pass
    monkeypatch.setattr(OpenAIService, "__init__", dummy_init)

    class DummyResponse:
        usage = types.SimpleNamespace(
            completion_tokens=1, prompt_tokens=2, total_tokens=3
        )
        message = types.SimpleNamespace(role="assistant", content="hi", tool_calls=None)
        choices = [types.SimpleNamespace(message=message)]
    monkeypatch.setattr(OpenAIService, "chat_completion", lambda self, req: DummyResponse())
    monkeypatch.setattr(OpenAIService, "responses", lambda self, req: (_ for _ in ()).throw(Exception("should not call responses")))

    adapter = OpenAIAdapter()
    request = TextRequest(
        provider=Provider(name="openai", model=ProviderModel(name="gpt-4o")),
        prompt=Prompt(
            parameter=PromptParameter(temperature=0.7, max_tokens=50),
            messages=[Message(role="user", content="hello")],
        ),
    )
    resp = adapter.generate_text(request)
    assert resp.prompt.messages[0].content == "hi"
    assert resp.usage.totalTokens == 3

def test_generate_text_gpt5(monkeypatch):
    def dummy_init(self):
        pass
    monkeypatch.setattr(OpenAIService, "__init__", dummy_init)
    monkeypatch.setattr(OpenAIService, "chat_completion", lambda self, req: (_ for _ in ()).throw(Exception("should not call chat_completion")))

    class DummyResponse:
        usage = types.SimpleNamespace(
            completion_tokens=4, prompt_tokens=5, total_tokens=9
        )
        output = [
            types.SimpleNamespace(
                role="assistant",
                content=[types.SimpleNamespace(text="world")],
            )
        ]
    monkeypatch.setattr(OpenAIService, "responses", lambda self, req: DummyResponse())

    adapter = OpenAIAdapter()
    request = TextRequest(
        provider=Provider(name="openai", model=ProviderModel(name="gpt-5")),
        prompt=Prompt(
            parameter=PromptParameter(temperature=0.5, max_tokens=60),
            messages=[Message(role="user", content="hi")],
        ),
    )
    resp = adapter.generate_text(request)
    assert resp.prompt.messages[0].content == "world"
    assert resp.usage.totalTokens == 9
