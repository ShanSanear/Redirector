import uuid

from pydantic import EmailStr, HttpUrl
from sqlalchemy import TypeDecorator, String
from sqlmodel import Field, Relationship, SQLModel, AutoString

class HttpUrlType(TypeDecorator):
    impl = String(2081)
    cache_ok = True
    python_type = HttpUrl

    def process_bind_param(self, value, dialect) -> str:
        return str(value)

    def process_result_value(self, value, dialect) -> HttpUrl:
        return HttpUrl(url=value)

    def process_literal_param(self, value, dialect) -> str:
        return str(value)


class RedirectEntryBase(SQLModel):
    name: str = Field(max_length=255, unique=True)
    target: HttpUrl = Field(max_length=255, sa_type=HttpUrlType)


class RedirectEntryCreate(RedirectEntryBase):
    ...


class RedirectEntryUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    target: HttpUrl | None = Field(default=None, max_length=255, sa_type=HttpUrlType)


class RedirectEntry(RedirectEntryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class RedirectEntryPublic(RedirectEntryBase):
    id: uuid.UUID


class RedirectEntriesPublic(SQLModel):
    redirects: list[RedirectEntryPublic]
    count: int



