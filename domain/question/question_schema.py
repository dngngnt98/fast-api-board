import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User


class Question(BaseModel):
    id: int
    subject: str
    content: str
    created_at: datetime.datetime
    answers: list[Answer]
    user: User | None
    modified_at: datetime.datetime | None = None


class QuestionCreate(BaseModel):
    subject: str
    content: str

    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class QuestionList(BaseModel):
    total: int
    question_list: list[Question] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int