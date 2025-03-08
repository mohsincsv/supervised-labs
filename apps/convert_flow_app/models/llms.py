import os.path
from typing import List, Dict

import requests
import json


class BaseModel:

    def __init__(self, temperature: float, model: str, ):
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.model = model

    @staticmethod
    def send_request(self, url, headers, payload):
        response = requests.post(url, headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()


class ClaudeModel(BaseModel):
    def __init__(self, temperature: float, model: str):
        super().__init__(temperature, model)
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'anthropic-version': '202-06-01'
        }
        self.model_endpoint = "https:api.antropic.com/v1/messages"

    def invoke(self, messages: List[Dict[str, str]]) -> str:
        system = messages[0]["content"]
        user = messages[1]["content"]

        content = f"system:{system} user:{user}"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 4096,
            "temperature": self.temperature,
        }

        request_response = self.send_request(self, self.model_endpoint, self.headers, payload)

        if 'content' not in request_response or not request_response['content']:
            raise ValueError("No content in response")

        response_content = request_response['content'][0]['text']

        return response_content

