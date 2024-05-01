import os
import json
import boto3

from dotenv import load_dotenv

from provider.bedrock.provider.antropic.model.request.claude_3_request import Claude3Request


class BedrockService():
    def __init__(self):
        self.load_env(".env.bedrock")

        self.client = boto3.client(
            service_name=os.getenv("BEDROCK_SERVICE_NAME"),
            region_name=os.getenv("BEDROCK_REGION_NAME")
        )

    def invoke_model(self, model: str, body_request: Claude3Request):
        return self.client.invoke_model(
                modelId=model,
                body=json.dumps(body_request.model_dump()),
            )
    
    def load_env(self, env_name: str) -> None:
        base_path = os.path.abspath(os.path.dirname(__file__))
        dotenv_path = os.path.join(base_path, "..", env_name)
        load_dotenv(dotenv_path)