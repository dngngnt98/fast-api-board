from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

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
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ""):
    total, _question_list = question_crud.get_question_list(
        db=db,
        skip=page * size,
        limit=size,
        keyword=keyword
    )

    return {
        'total': total,
        'question_list': _question_list
    }
# @router.get("/list", response_model=list[question_schema.Question])
# def question_list(db: Session = Depends(get_db)):
#     _question_list = question_crud.get_question_list(db)
#     return _question_list


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    _question = question_crud.get_question(db, question_id)
    return _question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session=Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db, _question_create, user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session=Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Question not found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not allowed to update this question")

    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session=Depends(get_db),
                    current_user: User=Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Question not found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not allowed to delete this question")
    question_crud.delete_question(db=db, db_question=db_question)
