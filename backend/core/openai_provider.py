import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from backend.core.llm_provider import LLMProvider


EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o-mini"


class OpenAIProvider(LLMProvider):

    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Set it in .env or pass api_key."
            )
        self.client = OpenAI(api_key=api_key)

    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:
        model_name = model or GENERATION_MODEL
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""

    def create_embedding(
        self,
        text: str,
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Text must not be empty.")

        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )
        return response.data[0].embedding

    def generate_text_with_fallback(
        self,
        prompt: str,
        models: Optional[List[str]] = None,
    ) -> str:
        model_list = models or [GENERATION_MODEL, "gpt-4o"]
        last_error = None

        for model_name in model_list:
            try:
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                )
                if response.choices[0].message.content:
                    return response.choices[0].message.content
            except Exception as error:
                last_error = error

        raise RuntimeError(
            f"Failed to generate text with all available models. "
            f"Last error: {last_error}"
        )
