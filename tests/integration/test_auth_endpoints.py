import pytest
from fastapi import HTTPException

from src.api import auth as auth_routes
from src.api.schemas import LoginRequest, UserPublic
from src.config.configuration import ConfigurationManager
from src.utils import get_db_connection, hash_password

TEST_USERNAME = "test-auth-integration-user"
TEST_PASSWORD = "test-password-123"


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
    """Stands in for a Starlette Request: only .session and .app.state are used by auth.py."""

    def __init__(self, api_config, session=None):
        self.session = session if session is not None else {}
        self.app = _FakeApp(api_config)


@pytest.fixture
def api_config():
    return ConfigurationManager().get_api_config()


@pytest.fixture
def users_table(api_config):
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
        conn.commit()
    finally:
        conn.close()

    yield

    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE username = %s", (TEST_USERNAME,))
        conn.commit()
    finally:
        conn.close()


@pytest.fixture
def test_user(api_config, users_table):
    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'user') RETURNING id",
                (TEST_USERNAME, hash_password(TEST_PASSWORD)),
            )
            user_id = cur.fetchone()[0]
        conn.commit()
    finally:
        conn.close()
    return user_id


def test_login_with_correct_credentials_sets_session(api_config, test_user):
    request = FakeRequest(api_config)
    credentials = LoginRequest(username=TEST_USERNAME, password=TEST_PASSWORD)

    user = auth_routes.login(credentials, request)

    assert user.username == TEST_USERNAME
    assert user.role == "user"
    assert request.session["user_id"] == test_user


def test_login_with_wrong_password_raises_401(api_config, test_user):
    request = FakeRequest(api_config)
    credentials = LoginRequest(username=TEST_USERNAME, password="wrong-password")

    with pytest.raises(HTTPException) as exc_info:
        auth_routes.login(credentials, request)
    assert exc_info.value.status_code == 401
    assert "user_id" not in request.session


def test_login_with_unknown_username_raises_401(api_config, users_table):
    request = FakeRequest(api_config)
    credentials = LoginRequest(username="no-such-user", password="whatever")

    with pytest.raises(HTTPException) as exc_info:
        auth_routes.login(credentials, request)
    assert exc_info.value.status_code == 401


def test_get_current_user_without_session_raises_401(api_config):
    request = FakeRequest(api_config)

    with pytest.raises(HTTPException) as exc_info:
        auth_routes.get_current_user(request)
    assert exc_info.value.status_code == 401


def test_get_current_user_with_valid_session_returns_user(api_config, test_user):
    request = FakeRequest(api_config, session={"user_id": test_user})

    user = auth_routes.get_current_user(request)

    assert user.id == test_user
    assert user.username == TEST_USERNAME


def test_get_current_user_with_deleted_user_id_raises_401(api_config, users_table):
    request = FakeRequest(api_config, session={"user_id": 999999})

    with pytest.raises(HTTPException) as exc_info:
        auth_routes.get_current_user(request)
    assert exc_info.value.status_code == 401


def test_logout_clears_session():
    request = FakeRequest(api_config=None, session={"user_id": 1})

    auth_routes.logout(request)

    assert request.session == {}


def test_require_admin_rejects_non_admin_user():
    user = UserPublic(id=1, username="plain-user", role="user")

    with pytest.raises(HTTPException) as exc_info:
        auth_routes.require_admin(user)
    assert exc_info.value.status_code == 403


def test_require_admin_accepts_admin_user():
    admin = UserPublic(id=1, username="admin-user", role="admin")

    assert auth_routes.require_admin(admin) == admin
