from fastapi import FastAPI
import sys, asyncio

from .utils.database import engine, Base
from app.endpoints import signup, login, random_password, configurations


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(random_password.router)
app.include_router(configurations.router)

# needed to run pytest
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
