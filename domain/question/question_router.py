from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_schema, question_crud

router = APIRouter(
    prefix="/api/question",
)


# @router.get("/list")
# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.created_at.desc()).all()
#     return _question_list

# Depends 사용 버전 (with와 같이 사용한 버전보다 더 간단하게 사용가능)
# response_model=list[question_schema.Question]
# 위의 구문의 의미는 question_list함수의 리턴값은 Question스키마로 구성된 리스트임을 의미
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    _question = question_crud.get_question(db, question_id)
    return _question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate, db: Session=Depends(get_db)):
    question_crud.create_question(db, _question_create)



