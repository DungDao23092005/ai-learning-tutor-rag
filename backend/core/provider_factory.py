import os
from typing import Optional

from backend.core.llm_provider import LLMProvider
from backend.core.gemini_provider import GeminiProvider
from backend.core.openai_provider import OpenAIProvider


def get_provider(provider_name: Optional[str] = None) -> LLMProvider:
    name = provider_name or os.getenv("LLM_PROVIDER", "gemini").lower()

    if name == "openai":
        return OpenAIProvider()
    return GeminiProvider()
