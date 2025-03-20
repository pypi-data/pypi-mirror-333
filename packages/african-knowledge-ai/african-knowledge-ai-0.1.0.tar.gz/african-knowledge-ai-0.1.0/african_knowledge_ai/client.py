import requests

class APIError(Exception):
    """Custom exception for API errors"""
    pass

class AfricanKnowledgeAIClient:
    def __init__(self, api_key: str, base_url="http://16.171.5.22:8000"):
        """Initialize African Knowledge AI SDK"""
        self.base_url = base_url
        self.api_key = api_key

    def request_model(self, model_name: str, file_path: str):
        """Send file to AI model and return the response"""
        url = f"{self.base_url}/ai/{model_name}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()  # Raise an error for bad responses
                return response.json()
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {e}")