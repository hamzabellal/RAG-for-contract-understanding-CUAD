from src.components.feedback_monitor import FeedbackMonitor


def test_build_stats_with_likes_and_dislikes():
    stats = FeedbackMonitor._build_stats({"like": 8, "dislike": 2})
    assert stats == {
        "like_count": 8,
        "dislike_count": 2,
        "total_feedback": 10,
        "like_ratio": 0.8,
    }


def test_build_stats_empty():
    stats = FeedbackMonitor._build_stats({})
    assert stats == {
        "like_count": 0,
        "dislike_count": 0,
        "total_feedback": 0,
        "like_ratio": None,
    }


def test_build_stats_likes_only():
    stats = FeedbackMonitor._build_stats({"like": 5})
    assert stats == {
        "like_count": 5,
        "dislike_count": 0,
        "total_feedback": 5,
        "like_ratio": 1.0,
    }
