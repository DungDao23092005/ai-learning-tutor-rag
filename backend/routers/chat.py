from fastapi import APIRouter, Depends, HTTPException

from backend.core.llm_provider import LLMProvider
from backend.core.provider_factory import get_provider
from backend.schemas.schemas import AskRequest, AskResponse, SourceChunk
from src.embedding import create_embedding
from src.rag_chain import build_rag_prompt
from src.vector_store import search_relevant_chunks


router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    provider: LLMProvider = Depends(get_provider),
):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    query_embedding = create_embedding(
        text=request.question,
        task_type="RETRIEVAL_QUERY",
    )

    retrieved_chunks = search_relevant_chunks(
        query_embedding=query_embedding,
        top_k=request.top_k,
    )

    if not retrieved_chunks:
        return AskResponse(
            answer="I cannot find relevant information in the uploaded document.",
            sources=[],
        )

    prompt = build_rag_prompt(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
    )

    answer = provider.generate_text_with_fallback(prompt)

    sources = [
        SourceChunk(
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            page_number=chunk["page_number"],
            chunk_index=chunk["chunk_index"],
            distance=chunk["distance"],
        )
        for chunk in retrieved_chunks
    ]

    return AskResponse(answer=answer, sources=sources)
