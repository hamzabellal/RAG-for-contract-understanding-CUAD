import psycopg2.extras
import pytest
from fastapi import HTTPException

from src.api import admin as admin_routes
from src.api.schemas import CreateUserRequest
from src.config.configuration import ConfigurationManager
from src.utils import get_db_connection

TEST_USERNAME = "test-admin-integration-user"


def _postgres_reachable() -> bool:
    try:
        conn = get_db_connection(ConfigurationManager().get_api_config())
        conn.close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _postgres_reachable(), reason="Postgres not reachable at configured host/port"
)


class _FakeState:
    def __init__(self, api_config):
        self.api_config = api_config


class _FakeApp:
    def __init__(self, api_config):
        self.state = _FakeState(api_config)


class FakeRequest:
    """Stands in for a Starlette Request: only .app.state is used by admin.py."""

    def __init__(self, api_config):
        self.app = _FakeApp(api_config)


@pytest.fixture
def api_config():
    return ConfigurationManager().get_api_config()


@pytest.fixture
def users_and_history_tables(api_config):
    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
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
        conn.commit()
    finally:
        conn.close()

    yield

    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM qa_history WHERE user_id IN (SELECT id FROM users WHERE username = %s)",
                (TEST_USERNAME,),
            )
            cur.execute("DELETE FROM users WHERE username = %s", (TEST_USERNAME,))
        conn.commit()
    finally:
        conn.close()


def test_create_user_persists_to_postgres(api_config, users_and_history_tables):
    request = FakeRequest(api_config)
    new_user = CreateUserRequest(username=TEST_USERNAME, password="irrelevant-pw", role="user")

    created = admin_routes.create_user(new_user, request)

    assert created.username == TEST_USERNAME
    assert created.role == "user"


def test_create_user_duplicate_username_raises_409(api_config, users_and_history_tables):
    request = FakeRequest(api_config)
    new_user = CreateUserRequest(username=TEST_USERNAME, password="irrelevant-pw", role="user")
    admin_routes.create_user(new_user, request)

    with pytest.raises(HTTPException) as exc_info:
        admin_routes.create_user(new_user, request)
    assert exc_info.value.status_code == 409


def test_list_users_includes_created_user(api_config, users_and_history_tables):
    request = FakeRequest(api_config)
    admin_routes.create_user(
        CreateUserRequest(username=TEST_USERNAME, password="pw", role="admin"), request
    )

    users = admin_routes.list_users(request)

    assert any(u.username == TEST_USERNAME and u.role == "admin" for u in users)


def test_admin_history_returns_only_requested_users_rows(api_config, users_and_history_tables):
    request = FakeRequest(api_config)
    created = admin_routes.create_user(
        CreateUserRequest(username=TEST_USERNAME, password="pw", role="user"), request
    )

    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO qa_history (user_id, timestamp, title, category, question, answer, contexts)
                VALUES (%s, now(), %s, %s, %s, %s, %s)
                """,
                (
                    created.id,
                    "test-contract",
                    "Governing Law",
                    "test question?",
                    "test answer.",
                    psycopg2.extras.Json(["context one", "context two"]),
                ),
            )
        conn.commit()
    finally:
        conn.close()

    entries = admin_routes.admin_history(created.id, request)

    assert len(entries) == 1
    assert entries[0].title == "test-contract"
    assert entries[0].contexts == ["context one", "context two"]


def test_admin_history_empty_for_user_with_no_questions(api_config, users_and_history_tables):
    request = FakeRequest(api_config)
    created = admin_routes.create_user(
        CreateUserRequest(username=TEST_USERNAME, password="pw", role="user"), request
    )

    entries = admin_routes.admin_history(created.id, request)

    assert entries == []
