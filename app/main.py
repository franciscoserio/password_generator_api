from fastapi import FastAPI

from .utils.database import engine, Base
from app.endpoints import signup, login, random_password, configurations


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(random_password.router)
app.include_router(configurations.router)
