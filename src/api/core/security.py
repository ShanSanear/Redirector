from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext
from sqlmodel import Session, select

from api.deps import SessionDep
from api.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


http_security = HTTPBasic()


def auth_user(session: SessionDep, credentials: Annotated[HTTPBasicCredentials, Depends(http_security)]):
    user = authenticate(session=session, username=credentials.username, password=credentials.password)
    return user.username


def superuser(user_object: Annotated[User | None, Depends(auth_user)]):
    if user_object:
        return user_object.is_superuser
    return False


def get_user_by_name(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_name(session=session, username=username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
