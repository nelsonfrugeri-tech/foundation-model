import google.genai as genai
from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import (
    TextResponse,
    Usage,
    Prompt,
    Message as MessageResponse,
    Tool as ToolResponse,
)


def serialize_request(text_request: TextRequest):
    messages = [
        {"role": msg.role, "parts": [{"text": msg.content}]}
        for msg in text_request.prompt.messages
    ]

    generation_config = {}
    if text_request.prompt.parameter is not None:
        if text_request.prompt.parameter.temperature is not None:
            generation_config["temperature"] = text_request.prompt.parameter.temperature
        if text_request.prompt.parameter.maxTokens is not None:
            generation_config["max_output_tokens"] = text_request.prompt.parameter.maxTokens
    generation_config = generation_config or None

    tools = None
    if text_request.tools:
        tool_list = []
        for tool in text_request.tools:
            params = None
            if tool.parameters is not None:
                params = {
                    "type": tool.parameters.type,
                    "properties": {
                        k: {
                            "type": v.type,
                            "description": v.description,
                            "enum": v.enum,
                        }
                        for k, v in tool.parameters.properties.items()
                    },
                    "required": tool.parameters.required or [],
                }
            func_decl = genai.types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=params,
            )
            tool_list.append(
                genai.types.Tool(function_declarations=[func_decl])
            )
        tools = tool_list

    return messages, generation_config, tools


def deserialize_response(response) -> TextResponse:
    usage = None
    if getattr(response, "usage_metadata", None):
        usage = Usage(
            completionTokens=response.usage_metadata.candidates_token_count,
            promptTokens=response.usage_metadata.prompt_token_count,
            totalTokens=response.usage_metadata.total_token_count,
        )

    messages = [
        MessageResponse(role="assistant", content=response.text)
    ]

    tools = []
    if response.candidates:
        candidate = response.candidates[0]
        for part in getattr(candidate.content, "parts", []):
            fc = getattr(part, "function_call", None)
            if fc is not None:
                arguments = fc.args or {}
                tools.append(
                    ToolResponse(name=fc.name, arguments=arguments)
                )
    return TextResponse(
        usage=usage,
        prompt=Prompt(messages=messages),
        tools=tools or None,
    )
