from fastapi import FastAPI

from .utils.database import engine, Base
from app.endpoints import signup, login


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
