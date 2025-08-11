import json
from typing import Any, List, Optional

from hub.api.adapter.http.v1.model.request.text_request import TextRequest
from hub.api.adapter.http.v1.model.response.text_response import (
    TextResponse,
    Tool as ToolResponse,
    Prompt,
    Message,
    Usage,
)

from provider.openai.adapter.model.request.chat_completion_request import (
    ChatCompletionRequest,
    Tool,
    Function,
    Parameters,
    Properties,
)
from provider.openai.adapter.model.request.responses_request import (
    ResponsesRequest,
    ResponseMessage,
    ResponseContent,
)
from provider.openai.service.openai_service import OpenAIService

from provider.port.interface_port import InterfacePort


class OpenAIAdapter(InterfacePort):
    def __init__(self) -> None:
        self.openai = OpenAIService()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        """Route requests to the appropriate OpenAI endpoint."""

        model_name = text_request_body.provider.model.name
        if "gpt-5" in model_name.lower():
            responses_request = ResponsesRequest(
                model=model_name,
                input=[
                    ResponseMessage(
                        role=msg.role,
                        content=[ResponseContent(text=msg.content)],
                    )
                    for msg in text_request_body.prompt.messages
                ],
            )
            self._set_parameters(text_request_body, responses_request)
            response = self.openai.responses(responses_request)
            return self._response_message_responses(response)

        chat_completion_request = ChatCompletionRequest(
            model=model_name,
            messages=[msg.model_dump() for msg in text_request_body.prompt.messages],
        )

        self._set_parameters(text_request_body, chat_completion_request)
        self._set_tools(text_request_body, chat_completion_request)

        response = self.openai.chat_completion(chat_completion_request)
        tool_calls = getattr(response.choices[0].message, "tool_calls", None)
        if tool_calls:
            return self._response_message_with_tools(response, tool_calls)
        return self._response_message(response)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _response_message_with_tools(self, response: Any, tool_calls: list) -> TextResponse:
        usage = Usage(
            completionTokens=response.usage.completion_tokens,
            promptTokens=response.usage.prompt_tokens,
            totalTokens=response.usage.total_tokens,
        )

        text_response = TextResponse(
            usage=usage,
            prompt=Prompt(messages=[Message(role=response.choices[0].message.role)]),
        )

        tools: List[ToolResponse] = [
            ToolResponse(name=tool.function.name, arguments=json.loads(tool.function.arguments))
            for tool in tool_calls
        ]
        if tools:
            text_response.tools = tools

        return text_response

    def _response_message(self, response: Any) -> TextResponse:
        usage = Usage(
            completionTokens=response.usage.completion_tokens,
            promptTokens=response.usage.prompt_tokens,
            totalTokens=response.usage.total_tokens,
        )

        prompt = Prompt(
            messages=[
                Message(
                    role=response.choices[0].message.role,
                    content=response.choices[0].message.content,
                )
            ]
        )

        return TextResponse(usage=usage, prompt=prompt)

    def _extract_output_text(self, response: Any) -> Optional[str]:
        """Best effort extraction of generated text from a Responses API result."""

        # 1) Prefer the SDK convenience properties
        for attr in ("output_text", "text"):
            val = getattr(response, attr, None)
            if isinstance(val, str) and val.strip():
                return val
        if isinstance(response, dict):
            for key in ("output_text", "text"):
                val = response.get(key)
                if isinstance(val, str) and val.strip():
                    return val

        # 2) Inspect "output" items which contain content blocks
        outputs = None
        if isinstance(response, dict):
            outputs = response.get("output") or response.get("outputs")
        else:
            outputs = getattr(response, "output", None) or getattr(response, "outputs", None)

        if outputs:
            for item in outputs:
                content = None
                if isinstance(item, dict):
                    content = item.get("content")
                else:
                    content = getattr(item, "content", None)
                if not content:
                    continue
                blocks = content if isinstance(content, list) else [content]
                for block in blocks:
                    txt = None
                    if isinstance(block, dict):
                        txt = block.get("text") or block.get("content")
                    else:
                        txt = getattr(block, "text", None) or getattr(block, "content", None)
                    if isinstance(txt, str) and txt.strip():
                        return txt

        # 3) Fall back to a recursive scan of any remaining dict structure
        data = None
        if isinstance(response, dict):
            data = response
        else:
            to_dict = getattr(response, "model_dump", None) or getattr(response, "dict", None)
            if callable(to_dict):
                try:
                    data = to_dict()
                except Exception:
                    data = None

        def scan(obj: Any) -> Optional[str]:
            if isinstance(obj, str) and obj.strip():
                return obj
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ("output_text", "text", "content"):
                        res = scan(v)
                        if res:
                            return res
                for v in obj.values():
                    res = scan(v)
                    if res:
                        return res
            if isinstance(obj, list):
                for v in obj:
                    res = scan(v)
                    if res:
                        return res
            return None

        if data is not None:
            found = scan(data)
            if found:
                return found

        return None

    def _response_message_responses(self, response: Any) -> TextResponse:
        usage_obj = getattr(response, "usage", None)
        usage = None
        if usage_obj is not None:
            completion = getattr(usage_obj, "output_tokens", None) or getattr(usage_obj, "completion_tokens", None)
            prompt = getattr(usage_obj, "input_tokens", None) or getattr(usage_obj, "prompt_tokens", None)
            total = getattr(usage_obj, "total_tokens", None)
            if total is None and completion is not None and prompt is not None:
                total = completion + prompt
            if completion is not None and prompt is not None and total is not None:
                usage = Usage(completionTokens=completion, promptTokens=prompt, totalTokens=total)

        content_text = self._extract_output_text(response) or ""
        prompt = Prompt(messages=[Message(role="assistant", content=content_text)])
        return TextResponse(usage=usage, prompt=prompt)

    def _set_tools(
        self,
        text_request_body: TextRequest,
        chat_completion_request: ChatCompletionRequest,
    ) -> None:
        tools = []
        if text_request_body.tools is not None:
            for tool in text_request_body.tools:
                properties = {}
                if tool.parameters is not None:
                    for key, property in tool.parameters.properties.items():
                        properties[key] = Properties(
                            type=property.type,
                            description=property.description,
                            enum=(property.enum if property.enum else []),
                        )

                tools.append(
                    Tool(
                        function=Function(
                            name=tool.name,
                            description=tool.description,
                            parameters=Parameters(
                                type=tool.parameters.type,
                                properties=properties,
                                required=(tool.parameters.required if tool.parameters.required else []),
                            ),
                        )
                    )
                )

        chat_completion_request.set_tools(
            tools=tools,
            tool_choice=text_request_body.tool_choice,
        )

    def _set_parameters(self, text_request_body: TextRequest, chat_completion_request: Any) -> None:
        if text_request_body.prompt.parameter is not None:
            if hasattr(chat_completion_request, "set_temperature"):
                chat_completion_request.set_temperature(
                    temperature=text_request_body.prompt.parameter.temperature
                )

            if hasattr(chat_completion_request, "set_max_tokens"):
                chat_completion_request.set_max_tokens(
                    max_tokens=text_request_body.prompt.parameter.maxTokens
                )

