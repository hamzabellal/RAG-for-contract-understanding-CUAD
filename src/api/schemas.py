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
