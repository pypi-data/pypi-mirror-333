import os
import requests

class AsyncUsageTracker:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def record_usage(self, service_name: str, tags: list, input_token: int, output_token: int, timestamp: str = None):
        url = f"{self.base_url}/usage"
        payload = {
            "service_name": service_name,
            "tags": tags,
            "input_token": input_token,
            "output_token": output_token,
        }
        if timestamp:
            payload["timestamp"] = timestamp
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_all_records(self):
        url = f"{self.base_url}/usage"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    
    def get_queue_size(self):
        url = f"{self.base_url}/queue-size"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
