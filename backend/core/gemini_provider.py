import os
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from backend.core.llm_provider import LLMProvider


EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


class GeminiProvider(LLMProvider):

    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY is missing. Set it in .env or pass api_key."
            )
        self.client = genai.Client(api_key=self.api_key)

    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:
        model_name = model or GENERATION_MODELS[0]
        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        return response.text or ""

    def create_embedding(
        self,
        text: str,
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Text must not be empty.")

        response = self.client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        return response.embeddings[0].values

    def generate_text_with_fallback(
        self,
        prompt: str,
        models: Optional[List[str]] = None,
    ) -> str:
        model_list = models or GENERATION_MODELS
        last_error = None

        for model_name in model_list:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response.text:
                    return response.text
            except Exception as error:
                last_error = error

        raise RuntimeError(
            f"Failed to generate text with all available models. "
            f"Last error: {last_error}"
        )
