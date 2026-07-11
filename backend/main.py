from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import chat, documents, quiz, summary


app = FastAPI(
    title="AI Learning Tutor RAG API",
    description="REST API for the AI Learning Tutor RAG system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(summary.router)
app.include_router(quiz.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "ai-learning-tutor-rag"}
