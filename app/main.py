from fastapi import FastAPI

from .utils.database import engine, Base
from app.endpoints import signup


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(signup.router)
