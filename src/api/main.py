from contextlib import asynccontextmanager
from datetime import UTC, datetime

import psycopg2.extras
from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.api import admin as admin_routes
from src.api import auth as auth_routes
from src.api.auth import get_current_user
from src.api.schemas import (
    AnswerResponse,
    FeedbackRequest,
    HistoryEntry,
    QuestionRequest,
    UserPublic,
)
from src.config.configuration import ConfigurationManager
from src.logger import logging
from src.pipeline.generation import GenerationPipeline
from src.utils import extract_category, get_db_connection, hash_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("loading retrieval and generation pipeline...")
    app.state.generator = GenerationPipeline().main()

    logging.info("preparing database tables...")
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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS qa_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    timestamp TIMESTAMPTZ NOT NULL,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    contexts JSONB NOT NULL
                )
            """)
            cur.execute("ALTER TABLE feedback ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)")

            cur.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                logging.info("no users found, seeding bootstrap admin account")
                cur.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin')",
                    (
                        app.state.api_config.bootstrap_admin_username,
                        hash_password(app.state.api_config.bootstrap_admin_password),
                    ),
                )
        conn.commit()
    finally:
        conn.close()

    logging.info("pipeline ready, API can serve requests")
    yield


app = FastAPI(title="CUAD RAG API", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=ConfigurationManager().get_api_config().session_secret_key)
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/contracts", response_model=list[str])
def list_contracts(user: UserPublic = Depends(get_current_user)):
    titles = app.state.generator.retriever.chunks_df["title"].unique().tolist()
    return sorted(titles)


@app.get("/history", response_model=list[HistoryEntry])
def my_history(user: UserPublic = Depends(get_current_user)):
    conn = get_db_connection(app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, timestamp, title, category, question, answer, contexts
                FROM qa_history WHERE user_id = %s ORDER BY timestamp DESC
                """,
                (user.id,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [
        HistoryEntry(id=r[0], timestamp=r[1], title=r[2], category=r[3], question=r[4], answer=r[5], contexts=r[6])
        for r in rows
    ]


@app.post("/contracts/{title}/questions", response_model=AnswerResponse)
def ask_question(title: str, request: QuestionRequest, user: UserPublic = Depends(get_current_user)):
    try:
        result = app.state.generator.generate(request.question, title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    category = extract_category(request.question) or ""
    conn = get_db_connection(app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qa_history (user_id, timestamp, title, category, question, answer, contexts)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user.id,
                    datetime.now(UTC),
                    title,
                    category,
                    request.question,
                    result["answer"],
                    psycopg2.extras.Json(result["contexts"]),
                ),
            )
        conn.commit()
    finally:
        conn.close()

    return AnswerResponse(answer=result["answer"], contexts=result["contexts"])


@app.post("/feedback")
def submit_feedback(feedback: FeedbackRequest, user: UserPublic = Depends(get_current_user)):
    conn = get_db_connection(app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO feedback (timestamp, title, question, answer, rating, comment, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(UTC),
                    feedback.title,
                    feedback.question,
                    feedback.answer,
                    feedback.rating,
                    feedback.comment,
                    user.id,
                ),
            )
        conn.commit()
    finally:
        conn.close()
    return {"status": "recorded"}


app.mount("/", StaticFiles(directory="src/frontend/static", html=True), name="static")
