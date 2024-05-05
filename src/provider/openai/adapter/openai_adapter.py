import json

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
from provider.openai.service.openai_service import OpenAIService

from provider.port.interface_port import InterfacePort


class OpenAIAdapter(InterfacePort):

    def __init__(self):
        self.openai = OpenAIService()

    def generate_text(self, text_request_body: TextRequest) -> TextResponse:
        chat_completion_request = ChatCompletionRequest(
                model=text_request_body.provider.model.name,
                messages=[
                    msg.model_dump() for msg in text_request_body.prompt.messages
                ],
            )

        self._set_parameters(
            text_request_body=text_request_body,
            chat_completion_request=chat_completion_request
        )
        
        self._set_tools(
            text_request_body=text_request_body,
            chat_completion_request=chat_completion_request
        )

        response = self.openai.chat_completion(chat_completion_request)

        return (
                self._response_message_with_tools(
                     response=response, 
                     tool_calls=response.choices[0].message.tool_calls 
                ) 
                if response.choices[0].message.tool_calls is not None
                else self._response_message(response)
            )

        
    def _response_message_with_tools(
            self, 
            response:dict, 
            tool_calls:list) -> TextResponse:

            tools = []
            text_response = TextResponse(
                usage=Usage(
                    completionTokens=response.usage.completion_tokens,
                    promptTokens=response.usage.prompt_tokens,
                    totalTokens=response.usage.total_tokens,
                ),
                prompt=Prompt(
                    messages=[
                        Message(
                            role=response.choices[0].message.role,
                        )
                    ]
                ),
            )

            for tool in tool_calls:
                tools.append(
                    ToolResponse(
                        name=tool.function.name,
                        arguments=json.loads(tool.function.arguments)
                    )
                )

            if len(tools) > 0:
                text_response.tools = tools

            return text_response

    def _response_message(self, response:dict) -> TextResponse:
        return TextResponse(
                usage=Usage(
                    completionTokens=response.usage.completion_tokens,
                    promptTokens=response.usage.prompt_tokens,
                    totalTokens=response.usage.total_tokens,
                ),
                prompt=Prompt(
                    messages=[
                        Message(
                            role=response.choices[0].message.role,
                            content=response.choices[0].message.content,
                        )
                    ]
                ),
            )
    
    def _set_tools(
            self, 
            text_request_body: TextRequest, 
            chat_completion_request: ChatCompletionRequest) -> None:

            tools = []
            if text_request_body.tools is not None:
                 for tool in text_request_body.tools:
                    
                    properties = {}
                    if tool.parameters is not None:
                        for key, property in tool.parameters.properties.items():
                            properties[key] = Properties(
                                type=property.type,
                                description=property.description,
                                enum=(
                                    property.enum
                                    if property.enum
                                    else []
                                )
                            )

                    tools.append(
                        Tool(
                            function=Function(
                                name=tool.name,
                                description=tool.description,
                                parameters=Parameters(
                                    type=tool.parameters.type,
                                    properties=properties,
                                    required=(
                                        tool.parameters.required
                                        if tool.parameters.required 
                                        else []
                                    )
                                )
                            )
                        )
                    )

            chat_completion_request.set_tools(
                tools=tools,
                tool_choice=text_request_body.tool_choice
            )            

    def _set_parameters(
            self, 
            text_request_body: TextRequest, 
            chat_completion_request: ChatCompletionRequest) -> None:
        
        if text_request_body.prompt.parameter is not None:
            chat_completion_request.set_temperature(
                temperature=text_request_body.prompt.parameter.temperature
            )

            chat_completion_request.set_max_tokens(
                max_tokens=text_request_body.prompt.parameter.maxTokens
            )
