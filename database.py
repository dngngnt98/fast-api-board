import contextlib

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlist3 데이터베이스의 파일을 의미하며 프로젝트 루트 디렉터리에 저장한다는 의미
SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-board.db"

# 커넥션 풀 생성
# 커넥션 풀: 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것을 말한다.
#          (즉, 데이터베이스에 접속하는 세션수를 제어하고, 또 세션 접속에 소요되는 시간을 줄이고자 하는 용도로 사용)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
## sqlalchemy + sqlite + alembic 조합 사용시 발생하는 문제 해결
## alembic은 제약조건 이름이 없으면 autogenerate 기능 오류가 발생하거나, diff를 인식하지 못한다.
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)


# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
