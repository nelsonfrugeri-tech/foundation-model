import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import generation_types
from google.generativeai.types import content_types


class GeminiService:
    def __init__(self) -> None:
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_KEY"))

    def generate(
        self,
        model: str,
        messages: list,
        generation_config: dict | None = None,
        tools: list | None = None,
        tool_choice: str | None = None,
    ) -> generation_types.GenerateContentResponse:
        tool_config = None
        if tools is not None and tool_choice is not None:
            tool_config = {
                "function_calling_config": {
                    "mode": tool_choice.upper()
                }
            }
        gen_model = genai.GenerativeModel(model)
        return gen_model.generate_content(
            messages,
            generation_config=generation_config,
            tools=tools,
            tool_config=tool_config,
        )
