import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import GenerateContentResponse


class GeminiService:
    def __init__(self) -> None:
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

    def generate(
        self,
        model: str,
        messages: list,
        generation_config: dict | None = None,
        tools: list | None = None,
        tool_choice: str | None = None,
    ) -> GenerateContentResponse:
        config = {}
        if generation_config:
            config.update(generation_config)
        if tools is not None:
            config["tools"] = tools
            if tool_choice is not None:
                config["tool_config"] = {
                    "function_calling_config": {
                        "mode": tool_choice.upper()
                    }
                }

        return self.client.models.generate_content(
            model=model,
            contents=messages,
            config=config or None,
        )
