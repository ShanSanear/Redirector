import secrets
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from api.core.config import settings
from api.crud import get_redirect_entry_by_name
from api.deps import SessionDep
from api.routes import api_router

security = HTTPBasic()
app = FastAPI(dependencies=[Depends(security)])
app.include_router(api_router, prefix=settings.API_V1_STR)


def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
# @app.get("/discord")
# async def redirect_discord():
#     return RedirectResponse("https://discord.gg/xDPWqhSj")

@app.get("/{entry_name}")
def redirect_to_place(session: SessionDep, entry_name: str):
    redirect_entry = get_redirect_entry_by_name(session=session, entry_name=entry_name)
    return RedirectResponse(redirect_entry.target)