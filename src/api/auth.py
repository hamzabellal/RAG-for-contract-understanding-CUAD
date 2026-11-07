from fastapi import APIRouter, Depends, HTTPException, Request

from src.api.schemas import LoginRequest, UserPublic
from src.utils import get_db_connection, verify_password

router = APIRouter()


def get_current_user(request: Request) -> UserPublic:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    conn = get_db_connection(request.app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return UserPublic(id=row[0], username=row[1], role=row[2])


def require_admin(user: UserPublic = Depends(get_current_user)) -> UserPublic:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user


@router.post("/auth/login", response_model=UserPublic)
def login(credentials: LoginRequest, request: Request):
    conn = get_db_connection(request.app.state.api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, username, role, password_hash FROM users WHERE username = %s",
                (credentials.username,),
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if row is None or not verify_password(credentials.password, row[3]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    request.session["user_id"] = row[0]
    return UserPublic(id=row[0], username=row[1], role=row[2])


@router.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"status": "logged out"}


@router.get("/auth/me", response_model=UserPublic)
def me(user: UserPublic = Depends(get_current_user)):
    return user
