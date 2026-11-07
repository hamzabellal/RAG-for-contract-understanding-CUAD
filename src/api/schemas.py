from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    contexts: list[str]


class FeedbackRequest(BaseModel):
    title: str
    question: str
    answer: str
    rating: Literal["like", "dislike"]
    comment: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    role: Literal["admin", "user"]


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: Literal["admin", "user"] = "user"


class HistoryEntry(BaseModel):
    id: int
    timestamp: datetime
    title: str
    category: str
    question: str
    answer: str
    contexts: list[str]


class FeedbackStats(BaseModel):
    like_count: int
    dislike_count: int
    total_feedback: int
    like_ratio: float | None
