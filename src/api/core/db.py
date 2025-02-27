from sqlmodel import create_engine

from .config import settings

engine = create_engine(str(settings.sqlalchemy_database_uri))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28

