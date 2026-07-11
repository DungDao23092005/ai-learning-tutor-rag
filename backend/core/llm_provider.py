from abc import ABC, abstractmethod
from typing import List, Optional


class LLMProvider(ABC):

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:
        ...

    @abstractmethod
    def create_embedding(
        self,
        text: str,
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> List[float]:
        ...

    @abstractmethod
    def generate_text_with_fallback(
        self,
        prompt: str,
        models: Optional[List[str]] = None,
    ) -> str:
        ...
