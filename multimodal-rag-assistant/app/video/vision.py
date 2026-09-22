import base64
from pathlib import Path

import requests


class VisionAnalyzer:

    def __init__(
        self,
        base_url: str,
        model: str,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def analyze(
        self,
        image_path: str,
    ) -> str:

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Frame not found: {image_path}"
            )

        image_data = base64.b64encode(
            path.read_bytes()
        ).decode("utf-8")

        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Analyze this video frame "
                        "for a multimodal RAG system. "
                        "Describe the important visible "
                        "objects, people, actions, text, "
                        "screens, diagrams, equipment, "
                        "and scene context. "
                        "Do not invent details."
                    ),
                    "images": [
                        image_data
                    ],
                }
            ],
        }

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"].strip()