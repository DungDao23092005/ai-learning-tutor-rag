from fastapi import APIRouter, HTTPException, UploadFile, File

from backend.schemas.schemas import (
    EmbedResponse,
    UploadResponse,
    VectorStoreStats,
)
from src.document_loader import get_document_stats, load_pdf_pages
from src.embedding import get_embedding_stats, create_embeddings_for_chunks
from src.text_splitter import get_chunk_stats, split_pages_into_chunks
from src.vector_store import (
    get_vector_store_stats,
    reset_vector_store,
    store_chunks_in_chroma,
)


router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    pages = load_pdf_pages(file_bytes)
    stats = get_document_stats(pages)

    return UploadResponse(
        message=f"Uploaded file: {file.filename}",
        total_pages=stats["total_pages"],
        pages_with_text=stats["pages_with_text"],
        total_words=stats["total_words"],
        total_characters=stats["total_characters"],
    )


@router.post("/process", response_model=EmbedResponse)
async def process_document(
    file: UploadFile = File(...),
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    pages = load_pdf_pages(file_bytes)
    chunks = split_pages_into_chunks(
        pages=pages,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunk_stats = get_chunk_stats(chunks)

    embedded_chunks = create_embeddings_for_chunks(chunks)
    embedding_stats = get_embedding_stats(embedded_chunks)

    reset_vector_store()
    stored_count = store_chunks_in_chroma(embedded_chunks)

    return EmbedResponse(
        message=f"Processed and stored {stored_count} chunks in ChromaDB.",
        total_embedded=stored_count,
        embedding_dimension=embedding_stats["embedding_dimension"],
    )


@router.get("/stats", response_model=VectorStoreStats)
async def get_stats():
    stats = get_vector_store_stats()
    return VectorStoreStats(
        collection_name=stats["collection_name"],
        total_items=stats["total_items"],
        persist_path=stats["persist_path"],
    )


@router.post("/reset")
async def reset_store():
    reset_vector_store()
    return {"message": "Vector store reset successfully."}
