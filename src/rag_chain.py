from typing import Dict, List

from src.embedding import get_gemini_client


GENERATION_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def generate_text_with_fallback(prompt: str) -> str:
    """
    Generate text with Gemini using multiple fallback models.
    """
    client = get_gemini_client()
    last_error = None

    for model_name in GENERATION_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as error:
            last_error = error

    raise RuntimeError(
        f"Failed to generate text with all available models. "
        f"Last error: {last_error}"
    )


def format_retrieved_context(retrieved_chunks: List[Dict]) -> str:
    """
    Format retrieved chunks into a context string for the LLM prompt.
    """
    if not retrieved_chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(retrieved_chunks, start=1):
        source_header = (
            f"[Source {index}] "
            f"Page: {chunk['page_number']}, "
            f"Chunk ID: {chunk['chunk_id']}"
        )

        context_parts.append(
            f"{source_header}\n{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)


def build_rag_prompt(question: str, retrieved_chunks: List[Dict]) -> str:
    """
    Build a RAG prompt using user question and retrieved context.
    """
    context = format_retrieved_context(retrieved_chunks)

    prompt = f"""
You are an AI learning tutor.

Your task is to answer the user's question using ONLY the provided document context.

Rules:
1. Use only the information from the context.
2. If the answer is not found in the context, say:
   "I cannot find this information in the uploaded document."
3. Do not invent facts.
4. Explain clearly and simply like a tutor.
5. If the user asks in Vietnamese, answer in Vietnamese.
6. If the user asks in English, answer in English.
7. At the end, mention which source pages were used.

Document context:
{context}

User question:
{question}

Answer:
"""
    return prompt.strip()


def generate_rag_answer(
    question: str,
    retrieved_chunks: List[Dict]
) -> str:
    """
    Generate an answer using Gemini based on retrieved chunks.
    """
    if not question or not question.strip():
        raise ValueError("Question must not be empty.")

    if not retrieved_chunks:
        return "I cannot find relevant information in the uploaded document."

    prompt = build_rag_prompt(
        question=question,
        retrieved_chunks=retrieved_chunks
    )

    return generate_text_with_fallback(prompt)


def generate_document_summary(
    chunks: List[Dict],
    max_chunks: int = 12
) -> str:
    """
    Generate a document summary from text chunks.

    To keep the prompt short, only the first max_chunks are used.
    """
    if not chunks:
        return "No document content is available for summarization."

    selected_chunks = chunks[:max_chunks]
    context = format_retrieved_context(selected_chunks)

    prompt = f"""
You are an AI learning tutor.

Summarize the uploaded learning document using ONLY the provided context.

Requirements:
1. Write the summary in Vietnamese.
2. Make it clear and easy for students to understand.
3. Include the main topic, key concepts, and important ideas.
4. Use bullet points when helpful.
5. Do not invent information outside the context.
6. At the end, mention the source pages used.

Document context:
{context}

Summary:
"""
    return generate_text_with_fallback(prompt.strip())