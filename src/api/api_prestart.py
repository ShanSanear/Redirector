from sqlmodel import Session

from core.config import settings
from core.security import get_user_by_name
from crud import create_user
from api.models import UserCreate


def init_db(session: Session) -> None:
    # TODO init db with alembic automation - somehow
    if settings.INIT_USERNAME:
        user_db = get_user_by_name(session=session, username=settings.INIT_USERNAME)
        if not user_db:
            create_user(session=session, user_create=UserCreate(username=settings.INIT_USERNAME, password=settings.INIT_PASSWORD))

