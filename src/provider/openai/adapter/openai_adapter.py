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
        """Extract textual content from an OpenAI Responses API result.

        The OpenAI SDK may return either Pydantic models or plain dictionaries.
        This helper normalises both cases and searches for the generated text in
        the most common locations.
        """

        # 0) normalise to dict when possible
        as_dict = response if isinstance(response, dict) else None
        if as_dict is None:
            to_dict = getattr(response, "model_dump", None) or getattr(response, "dict", None)
            if callable(to_dict):
                try:
                    as_dict = to_dict()
                except Exception:
                    as_dict = None

        # 1) direct ``output_text`` property
        text = response.get("output_text") if isinstance(response, dict) else getattr(response, "output_text", None)
        if not text and isinstance(as_dict, dict):
            text = as_dict.get("output_text")
        if text:
            return text

        # 2) iterate over ``output`` items
        output = response.get("output") if isinstance(response, dict) else getattr(response, "output", None)
        if not output and isinstance(as_dict, dict):
            output = as_dict.get("output")

        parts: List[str] = []

        def add_txt(val: Any) -> None:
            if isinstance(val, str) and val:
                parts.append(val)

        if output:
            for item in output:
                txt = getattr(item, "text", None) if not isinstance(item, dict) else item.get("text")
                add_txt(txt)

                content = getattr(item, "content", None) if not isinstance(item, dict) else item.get("content")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, str):
                            add_txt(c)
                        elif isinstance(c, dict):
                            add_txt(c.get("text"))
                            add_txt(c.get("content"))
                            add_txt(c.get("output_text"))
                        else:
                            add_txt(getattr(c, "text", None))
                            inner = getattr(c, "content", None)
                            if isinstance(inner, str):
                                add_txt(inner)
                elif isinstance(content, dict):
                    add_txt(content.get("text"))
                    add_txt(content.get("content"))
                    add_txt(content.get("output_text"))
                elif isinstance(content, str):
                    add_txt(content)

        if parts:
            return "\n".join(p for p in parts if p)

        # 3) check for ``message`` attribute
        message = response.get("message") if isinstance(response, dict) else getattr(response, "message", None)
        if not message and isinstance(as_dict, dict):
            message = as_dict.get("message")
        if message:
            if isinstance(message, dict):
                add_txt(message.get("content"))
                add_txt(message.get("text"))
            else:
                add_txt(getattr(message, "content", None))
                add_txt(getattr(message, "text", None))
            if parts:
                return "\n".join(p for p in parts if p)

        # 4) final fallback: scan dict for plausible keys
        def scan_dict(d: dict) -> None:
            for k, v in d.items():
                if isinstance(v, str) and k in ("output_text", "text", "content") and v:
                    parts.append(v)
                elif isinstance(v, dict):
                    scan_dict(v)
                elif isinstance(v, list):
                    for it in v:
                        if isinstance(it, dict):
                            scan_dict(it)

        if isinstance(as_dict, dict):
            scan_dict(as_dict)
            if parts:
                return "\n".join(p for p in parts if p)

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

