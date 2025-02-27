from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from api.core.config import settings
import api.crud
from api.core.security import http_security
from api.deps import SessionDep
from api.routes import api_router

app = FastAPI(dependencies=[Depends(http_security)])
app.include_router(api_router, prefix=settings.API_V1_STR)


# @app.get("/users/me")
# def read_current_user(user_permissions: Annotated[User, Depends(auth_user)]) -> User:
#     return user_permissions
#
@app.get("/{entry_name}")
def redirect_to_place(session: SessionDep, entry_name: str):
    redirect_entry = api.crud.get_redirect_entry_by_name(session=session, entry_name=entry_name)
    return RedirectResponse(redirect_entry.target)