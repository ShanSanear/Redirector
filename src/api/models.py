import uuid

from pydantic import HttpUrl
from sqlalchemy import TypeDecorator, String
from sqlmodel import Field, SQLModel

# Shared properties
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=64)
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    password: str = Field(min_length=8, max_length=40)
    username: str  = Field(max_length=64)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    username: str | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


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



