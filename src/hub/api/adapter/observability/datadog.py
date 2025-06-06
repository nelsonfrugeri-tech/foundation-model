# Reexecutar o código após o reset do ambiente
import sys
import json
import logging
import requests
import os

class DatadogLogAgent:
    def __init__(self, datadog_api_key: str):
        self.api_key = datadog_api_key
        self.datadog_url = "https://http-intake.logs.datadoghq.com/v1/input"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "DD-API-KEY": self.api_key
        })

    def send_log(self, log: dict):
        try:
            payload = json.dumps(log)
            response = self.session.post(self.datadog_url, data=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"[Datadog Agent] Error sending log: {e}")

class StdoutInterceptor:
    def __init__(self, agent: DatadogLogAgent):
        self.agent = agent

    def write(self, message):
        if message.strip():
            try:
                log = json.loads(message)
                self.agent.send_log(log)
            except json.JSONDecodeError:
                pass  # Ignore non-JSON logs

    def flush(self):
        pass

def start_agent():
    api_key = os.getenv("DATADOG_API_KEY")
    if not api_key:
        print("[Datadog Agent] DATADOG_API_KEY not set")
        return

    agent = DatadogLogAgent(api_key)
    sys.stdout = StdoutInterceptor(agent)

