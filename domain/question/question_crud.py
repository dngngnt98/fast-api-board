from models import Question
from domain.question.question_schema import QuestionCreate
from sqlalchemy.orm import Session
from datetime import datetime


def get_question_list(db: Session):
    _question_list = (db.query(Question)
                      .order_by(Question.created_at.desc())
                      .all())
    return _question_list


def get_question(db: Session, question_id: int):
    _question = db.query(Question).get(question_id)
    return _question


def create_question(db: Session, _question_create: QuestionCreate):
    db_question = Question(
        subject=_question_create.subject,
        content=_question_create.content,
        created_at=datetime.now()
    )

    db.add(db_question)
    db.commit()