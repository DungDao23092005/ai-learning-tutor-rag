from typing import Dict, List, Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    total_pages: int
    pages_with_text: int
    total_words: int
    total_characters: int


class EmbedRequest(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200


class EmbedResponse(BaseModel):
    message: str
    total_embedded: int
    embedding_dimension: int


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class SourceChunk(BaseModel):
    chunk_id: str
    text: str
    page_number: int
    chunk_index: int
    distance: float


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]


class SummaryRequest(BaseModel):
    max_chunks: int = 12


class SummaryResponse(BaseModel):
    summary: str


class QuizRequest(BaseModel):
    number_of_questions: int = 5


class QuizQuestion(BaseModel):
    question: str
    options: Dict[str, str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


class CheckQuizRequest(BaseModel):
    questions: List[QuizQuestion]
    user_answers: Dict[int, str]


class CheckQuizResponse(BaseModel):
    score: int
    total: int
    results: List[Dict]


class StoreResponse(BaseModel):
    message: str
    stored_count: int


class VectorStoreStats(BaseModel):
    collection_name: str
    total_items: int
    persist_path: str
