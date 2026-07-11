from fastapi import APIRouter, Depends, HTTPException

from backend.core.llm_provider import LLMProvider
from backend.core.provider_factory import get_provider
from backend.schemas.schemas import SummaryRequest, SummaryResponse
from src.rag_chain import generate_document_summary as generate_summary


router = APIRouter(prefix="/api/summary", tags=["summary"])


@router.post("/generate", response_model=SummaryResponse)
async def generate_summary_endpoint(
    request: SummaryRequest,
    provider: LLMProvider = Depends(get_provider),
):
    from src.text_splitter import get_chunk_stats
    from src.vector_store import get_or_create_collection

    collection = get_or_create_collection()
    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No document chunks found. Upload and process a document first.",
        )

    all_data = collection.get(include=["documents", "metadatas"])
    chunks = []
    for idx, doc_id in enumerate(all_data["ids"]):
        chunks.append({
            "chunk_id": doc_id,
            "text": all_data["documents"][idx],
            "page_number": all_data["metadatas"][idx].get("page_number", 0),
            "chunk_index": all_data["metadatas"][idx].get("chunk_index", 0),
        })

    summary = generate_summary(chunks, max_chunks=request.max_chunks)
    return SummaryResponse(summary=summary)
