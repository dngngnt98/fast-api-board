import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer


class Question(BaseModel):
    id: int
    subject: str
    content: str
    created_at: datetime.datetime
    answers: list[Answer]


class QuestionCreate(BaseModel):
    subject: str
    content: str

    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v