import types
import sys
import os
sys.path.insert(0, os.path.abspath('src'))
import google.genai as genai
from provider.gemini.adapter.gemini_adapter import GeminiAdapter
from hub.api.adapter.http.v1.model.request.text_request import (
    TextRequest, Provider, ProviderModel, Prompt, PromptParameter, Message
)


class DummyModels:
    def generate_content(self, model, contents, config=None):
        class Usage:
            prompt_token_count = 75
            candidates_token_count = 8
            total_token_count = 83

        class FunctionCall:
            name = "get_weather"
            args = {"city": "Paris"}

        class Part:
            function_call = FunctionCall()

        class Candidate:
            content = types.SimpleNamespace(parts=[Part()])

        return types.SimpleNamespace(
            text="A capital da França é Paris.",
            candidates=[Candidate()],
            usage_metadata=Usage(),
        )


class DummyClient:
    def __init__(self, *args, **kwargs):
        self.models = DummyModels()

def test_generate_text(monkeypatch):
    monkeypatch.setenv("GEMINI_KEY", "dummy")
    monkeypatch.setattr(genai, 'Client', lambda *a, **k: DummyClient())
    adapter = GeminiAdapter()
    request = TextRequest(
        provider=Provider(name="gemini", model=ProviderModel(name="gemini-2.0-pro")),
        prompt=Prompt(
            parameter=PromptParameter(temperature=0.7, max_tokens=150),
            messages=[Message(role="user", content="Qual a capital da França?")]
        ),
        tool_choice="auto",
    )
    resp = adapter.generate_text(request)
    assert resp.prompt.messages[0].content == "A capital da França é Paris."
    assert resp.usage.totalTokens == 83
    assert resp.tools[0].name == "get_weather"
    assert resp.tools[0].arguments == {"city": "Paris"}
