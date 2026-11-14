import pytest

from src.api import main as api_main
from src.api.schemas import FeedbackRequest, UserPublic
from src.config.configuration import ConfigurationManager
from src.utils import get_db_connection

TEST_USER = UserPublic(id=1, username="test-user", role="user")

TEST_TITLE = "test-integration-contract"


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


@pytest.fixture
def api_config():
    return ConfigurationManager().get_api_config()


@pytest.fixture
def feedback_table(api_config):
    conn = get_db_connection(api_config)
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
                    comment TEXT,
                    user_id INTEGER
                )
            """)
        conn.commit()
    finally:
        conn.close()

    yield

    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM feedback WHERE title = %s", (TEST_TITLE,))
        conn.commit()
    finally:
        conn.close()


def test_submit_feedback_writes_to_postgres(api_config, feedback_table):
    api_main.app.state.api_config = api_config

    request = FeedbackRequest(
        title=TEST_TITLE,
        question="test question?",
        answer="test answer",
        rating="like",
        comment=None,
    )

    result = api_main.submit_feedback(request, user=TEST_USER)
    assert result == {"status": "recorded"}

    conn = get_db_connection(api_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title, rating FROM feedback WHERE title = %s ORDER BY id DESC LIMIT 1",
                (TEST_TITLE,),
            )
            row = cur.fetchone()
    finally:
        conn.close()

    assert row == (TEST_TITLE, "like")
