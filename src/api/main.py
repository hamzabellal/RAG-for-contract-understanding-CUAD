import csv
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from src.api.schemas import AnswerResponse, FeedbackRequest, QuestionRequest
from src.logger import logging
from src.pipeline.generation import GenerationPipeline

FEEDBACK_PATH = Path("artifacts/feedback/feedback.csv")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("loading retrieval and generation pipeline...")
    app.state.generator = GenerationPipeline().main()
    logging.info("pipeline ready, API can serve requests")
    yield


app = FastAPI(title="CUAD RAG API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/contracts/{title}/questions", response_model=AnswerResponse)
def ask_question(title: str, request: QuestionRequest):
    try:
        result = app.state.generator.generate(request.question, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return AnswerResponse(answer=result["answer"], contexts=result["contexts"])


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = FEEDBACK_PATH.exists()
    with open(FEEDBACK_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "title", "question", "answer", "rating", "comment"])
        writer.writerow([
            datetime.now(UTC).isoformat(),
            feedback.title,
            feedback.question,
            feedback.answer,
            feedback.rating,
            feedback.comment or "",
        ])
    return {"status": "recorded"}


app.mount("/", StaticFiles(directory="src/frontend/static", html=True), name="static")
