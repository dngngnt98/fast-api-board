from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 질문 모델
class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)


class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    # 답변 모델에서 질문 모델을 참조하기 위해 추가
    # relationship으로 question 속성을 생성하면 답변 객체에서 연결된 질문의 제목을 answer.question.subject처럼 참조가 가능하다
    # relationship('참조할 모델명', '역참조 설정')
    question = relationship('Question', backref='answers')