import requests

from app.llm.base import LLMInterface


class OllamaLLM(LLMInterface):

    def __init__(
        self,
        base_url: str,
        model: str,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"].strip()