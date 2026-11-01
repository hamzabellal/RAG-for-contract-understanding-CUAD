from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from src.api.schemas import AnswerResponse, FeedbackRequest, QuestionRequest
from src.logger import logging
from src.pipeline.generation import GenerationPipeline
from src.config.configuration import ConfigurationManager
from src.utils import get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("loading retrieval and generation pipeline...")
    app.state.generator = GenerationPipeline().main()

    logging.info("preparing feedback table...")
    app.state.api_config = ConfigurationManager().get_api_config()
    conn = get_db_connection(app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL,
                    title TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    comment TEXT
                )
            """)
        conn.commit()
    finally:
        conn.close()

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
    conn = get_db_connection(app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO feedback (timestamp, title, question, answer, rating, comment)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(UTC),
                    feedback.title,
                    feedback.question,
                    feedback.answer,
                    feedback.rating,
                    feedback.comment,
                ),
            )
        conn.commit()
    finally:
        conn.close()
    return {"status": "recorded"}


app.mount("/", StaticFiles(directory="src/frontend/static", html=True), name="static")
