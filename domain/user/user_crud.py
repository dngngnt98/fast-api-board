from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
from datetime import datetime

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        email=str(user_create.email),
        created_at=datetime.now()
    )

    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email)
    ).first()


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()