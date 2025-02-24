import uuid

from fastapi import HTTPException
from sqlmodel import Session, select

from .models import RedirectEntry, RedirectEntryCreate, RedirectEntryUpdate


def read_redirects(*, session: Session, skip: int = 0, limit: int = 100,) -> list[RedirectEntry]:
    statement = select(RedirectEntry).offset(skip).limit(limit)
    redirects = session.exec(statement).all()
    return redirects

def create_redirect_entry(*, session: Session, redirect_entry_create: RedirectEntryCreate) -> RedirectEntry:
    db_obj = RedirectEntry.model_validate(redirect_entry_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_redirect_entry(*, session: Session, entry_id: uuid.UUID) -> RedirectEntry:
    redirect_entry = session.get(RedirectEntry, entry_id)
    if not redirect_entry:
        raise HTTPException(status_code=404, detail="Redirect entry not found")
    return redirect_entry


def update_redirect_entry(*, session: Session, entry_id: uuid.UUID,
                          redirect_entry_in: RedirectEntryUpdate) -> RedirectEntry:
    redirect_entry_db = get_redirect_entry(session=session, entry_id=entry_id)
    redirect_entry_data = redirect_entry_in.model_dump(exclude_unset=True)
    redirect_entry_db.sqlmodel_update(redirect_entry_data)
    session.add(redirect_entry_db)
    session.commit()
    session.refresh(redirect_entry_db)
    return redirect_entry_db


def delete_redirect_entry(*, session: Session, entry_id: uuid.UUID):
    redirect_entry = session.get(RedirectEntry, entry_id)
    if not redirect_entry:
        raise HTTPException(status_code=404, detail="Redirect entry not found")
    session.delete(redirect_entry)
    session.commit()

def get_redirect_entry_by_name(*, session: Session, entry_name: str) -> RedirectEntry:
    statement = select(RedirectEntry).where(RedirectEntry.name == entry_name)
    redirect_entry = session.exec(statement).first()
    if not redirect_entry:
        raise HTTPException(status_code=404, detail="Redirect entry not found")
    return redirect_entry