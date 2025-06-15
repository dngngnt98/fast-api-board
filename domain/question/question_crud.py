from models import Question, User, Answer
from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ""):
    question_list = db.query(Question)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)) \
            .subquery()

        question_list = question_list.outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )

    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.created_at.desc()) \
        .offset(skip).limit(limit).distinct().all()
    return total, question_list


def get_question(db: Session, question_id: int):
    _question = db.query(Question).get(question_id)
    return _question


def create_question(db: Session, _question_create: QuestionCreate, user: User):
    db_question = Question(
        subject=_question_create.subject,
        content=_question_create.content,
        created_at=datetime.now(),
        user=user
    )

    db.add(db_question)
    db.commit()


def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modified_at = datetime.now()
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


def search_question(db: Session, page: int = 0, limit: int = 10, keyword: str = ""):
    question_list = db.query(Question)
    print(keyword)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)) \
            .subquery()

        question_list = question_list.outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |
                    Question.content.ilike(search) |
                    User.username.ilike(search) |
                    sub_query.c.content.ilike(search) |
                    sub_query.c.username.ilike(search)
                    )

    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.created_at.desc()) \
        .offset(page).limit(limit).distinct().all()
    return total, question_list


