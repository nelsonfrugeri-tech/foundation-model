import os
import json
import boto3

from foundation_model.bedrock.adapter.model.request.body_request import BodyRequest

class BedrockService():
    def __init__(self):
        self.client = boto3.client(
            service_name=os.getenv("BEDROCK_SERVICE_NAME"),
            region_name=os.getenv("BEDROCK_REGION_NAME")
        )

    def invoke_model(self, model: str, body_request: BodyRequest):
        return self.client.invoke_model(
                modelId=model,
                body=json.dumps(body_request.model_dump()),
            )