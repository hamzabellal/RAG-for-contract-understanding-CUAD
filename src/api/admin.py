import psycopg2.errors
from fastapi import APIRouter, Depends, HTTPException, Request

from src.api.auth import require_admin
from src.api.schemas import CreateUserRequest, FeedbackStats, HistoryEntry, UserPublic
from src.components.feedback_monitor import FeedbackMonitor
from src.config.configuration import ConfigurationManager
from src.utils import get_db_connection, hash_password

router = APIRouter(dependencies=[Depends(require_admin)])


@router.post("/admin/users", response_model=UserPublic, status_code=201)
def create_user(new_user: CreateUserRequest, request: Request):
    conn = get_db_connection(request.app.state.api_config)
    try:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id",
                    (new_user.username, hash_password(new_user.password), new_user.role),
                )
            except psycopg2.errors.UniqueViolation as e:
                conn.rollback()
                raise HTTPException(status_code=409, detail="Username already exists") from e
            user_id = cur.fetchone()[0]
        conn.commit()
    finally:
        conn.close()
    return UserPublic(id=user_id, username=new_user.username, role=new_user.role)


@router.get("/admin/users", response_model=list[UserPublic])
def list_users(request: Request):
    conn = get_db_connection(request.app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, role FROM users ORDER BY username")
            rows = cur.fetchall()
    finally:
        conn.close()
    return [UserPublic(id=r[0], username=r[1], role=r[2]) for r in rows]


@router.get("/admin/history", response_model=list[HistoryEntry])
def admin_history(user_id: int, request: Request):
    conn = get_db_connection(request.app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, timestamp, title, category, question, answer, contexts
                FROM qa_history WHERE user_id = %s ORDER BY timestamp DESC
                """,
                (user_id,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return [
        HistoryEntry(id=r[0], timestamp=r[1], title=r[2], category=r[3], question=r[4], answer=r[5], contexts=r[6])
        for r in rows
    ]


@router.get("/admin/feedback-stats", response_model=FeedbackStats)
def feedback_stats():
    monitoring_config = ConfigurationManager().get_monitoring_config()
    stats = FeedbackMonitor(monitoring_config).compute_like_ratio()
    return FeedbackStats(**stats)
