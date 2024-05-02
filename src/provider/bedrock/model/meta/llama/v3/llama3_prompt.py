from provider.bedrock.model.meta.llama.v3.llama3_tool import Tools


class Llama3Prompt:

    @classmethod
    def completion(cls, messages: str) -> str:
        return f"""
            <|begin_of_text|>
            <|start_header_id|>user<|end_header_id|>
            {messages}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
        """
    
    @classmethod
    def function_calling(cls, messages: str, tools: list) -> str:
        return f"""
            <|im_start|>system
            You are an assistant and must help the user with their doubts and questions.            
            You are provided with function signatures within <tools></tools>.
            What are tools? Tools are software configurations such as APIs that can be run later to find the answer, if you don't have the answer try to understand if some of the tools can be run.
            Here are the available tools: <tools>{tools}</tools>.
            If the response is one or more tools, it only responds with a json schema of the pydantic model for each tool that can be called: {Tools}.
            If you're not sure if the answer is a tool, simply answer.<|im_end|>
            <|begin_of_text|>
            <|start_header_id|>user<|end_header_id|>
            {messages}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
        """