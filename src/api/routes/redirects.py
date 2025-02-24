import uuid

from fastapi import APIRouter
from sqlmodel import select, Session
from starlette.responses import RedirectResponse

from ..deps import SessionDep
from ..models import RedirectEntriesPublic, RedirectEntry, RedirectEntryCreate, RedirectEntryUpdate
from ..crud import read_redirects, get_redirect_entry, create_redirect_entry, delete_redirect_entry, \
    update_redirect_entry, get_redirect_entry_by_name

router = APIRouter(prefix="/redirects", tags=["redirects"])


@router.get("/", response_model=RedirectEntriesPublic)
def get_redirects(
        session: SessionDep, skip: int = 0, limit: int = 100,
) -> RedirectEntriesPublic:
    redirects = read_redirects(session=session, skip=skip, limit=limit)
    return RedirectEntriesPublic(redirects=redirects, count=len(redirects))

@router.get("/{entry_id}", response_model=RedirectEntry)
def get_redirect(session: SessionDep, entry_id: uuid.UUID) -> RedirectEntry:
    return get_redirect_entry(session=session, entry_id=entry_id)

@router.post("/", response_model=RedirectEntry, status_code=201)
def create_redirect(session: SessionDep, redirect_model: RedirectEntryCreate) -> RedirectEntry:
    model = create_redirect_entry(session=session, redirect_entry_create=redirect_model)
    return model

@router.delete("/{entry_id}", status_code=204)
def delete_redirect(session: SessionDep, entry_id: uuid.UUID):
    delete_redirect_entry(session=session, entry_id=entry_id)

@router.patch("/{entry_id}", response_model=RedirectEntry, status_code=200)
def update_redirect(session: SessionDep, entry_id: uuid.UUID, redirect_model: RedirectEntryUpdate) -> RedirectEntry:
    model = update_redirect_entry(session=session, entry_id=entry_id, redirect_entry_in=redirect_model)
    return model
