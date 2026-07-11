import asyncio
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types


EMBEDDING_MODEL = "gemini-embedding-001"
_MAX_WORKERS = 5


def get_gemini_client() -> genai.Client:
    """
    Create a Gemini client from GOOGLE_API_KEY in .env file.
    """
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Please create a .env file "
            "and add your Gemini API key."
        )

    return genai.Client(api_key=api_key)


def create_embedding(
    text: str,
    task_type: str = "RETRIEVAL_DOCUMENT"
) -> List[float]:
    """
    Create an embedding vector for a single text.

    Args:
        text: Input text.
        task_type: Embedding task type.
                   For document chunks, use RETRIEVAL_DOCUMENT.
                   For user questions, use RETRIEVAL_QUERY later.

    Returns:
        A list of float numbers representing the embedding vector.
    """
    if not text or not text.strip():
        raise ValueError("Text must not be empty.")

    client = get_gemini_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type
        )
    )

    return response.embeddings[0].values


def create_embeddings_for_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Create embeddings for all text chunks.

    Args:
        chunks: List of chunk dictionaries from text_splitter.py

    Returns:
        A new list of chunks with an extra 'embedding' field.
    """
    embedded_chunks = []

    for chunk in chunks:
        embedding = create_embedding(
            text=chunk["text"],
            task_type="RETRIEVAL_DOCUMENT"
        )

        embedded_chunk = {
            **chunk,
            "embedding": embedding,
        }

        embedded_chunks.append(embedded_chunk)

    return embedded_chunks


def create_embeddings_for_chunks_parallel(chunks: List[Dict]) -> List[Dict]:
    """
    Create embeddings for all text chunks using a thread pool.

    This reduces total processing time when embedding many chunks
    by running up to _MAX_WORKERS API calls concurrently.

    Args:
        chunks: List of chunk dictionaries from text_splitter.py

    Returns:
        A new list of chunks with an extra 'embedding' field.
    """
    if not chunks:
        return []

    embedded_chunks = [None] * len(chunks)

    with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
        future_map = {}

        for index, chunk in enumerate(chunks):
            future = executor.submit(
                create_embedding,
                text=chunk["text"],
                task_type="RETRIEVAL_DOCUMENT",
            )
            future_map[future] = (index, chunk)

        for future in as_completed(future_map):
            index, chunk = future_map[future]
            embedding = future.result()
            embedded_chunks[index] = {**chunk, "embedding": embedding}

    return embedded_chunks


async def create_embeddings_for_chunks_async(chunks: List[Dict]) -> List[Dict]:
    """
    Async wrapper around create_embeddings_for_chunks_parallel.

    Uses asyncio.to_thread to offload the thread-pool work
    without blocking the async event loop (useful in FastAPI endpoints).
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, create_embeddings_for_chunks_parallel, chunks
    )


def get_embedding_stats(embedded_chunks: List[Dict]) -> Dict:
    """
    Calculate simple statistics for embedded chunks.
    """
    if not embedded_chunks:
        return {
            "total_embedded_chunks": 0,
            "embedding_dimension": 0,
        }

    first_embedding = embedded_chunks[0]["embedding"]

    return {
        "total_embedded_chunks": len(embedded_chunks),
        "embedding_dimension": len(first_embedding),
    }