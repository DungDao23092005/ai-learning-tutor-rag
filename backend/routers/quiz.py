from fastapi import APIRouter, HTTPException

from backend.schemas.schemas import (
    CheckQuizRequest,
    CheckQuizResponse,
    QuizQuestion,
    QuizRequest,
    QuizResponse,
)
from src.quiz_generator import check_quiz_answers, generate_quiz


router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz_endpoint(request: QuizRequest):
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

    questions = generate_quiz(chunks, number_of_questions=request.number_of_questions)
    return QuizResponse(questions=questions)


@router.post("/check", response_model=CheckQuizResponse)
async def check_answers_endpoint(request: CheckQuizRequest):
    results = check_quiz_answers(
        quiz_questions=[q.dict() for q in request.questions],
        user_answers=request.user_answers,
    )
    return CheckQuizResponse(
        score=results["score"],
        total=results["total"],
        results=results["results"],
    )
