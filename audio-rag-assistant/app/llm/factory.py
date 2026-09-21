import os

from app.llm.base import LLMInterface
from app.llm.ollama import OllamaLLM


def create_llm() -> LLMInterface:

    provider = os.getenv(
        "LLM_PROVIDER",
        "ollama",
    ).lower()

    if provider == "ollama":

        return OllamaLLM(
            base_url=os.getenv(
                "OLLAMA_URL",
                "http://localhost:11434",
            ),
            model=os.getenv(
                "OLLAMA_MODEL",
                "llama3.2",
            ),
        )

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )