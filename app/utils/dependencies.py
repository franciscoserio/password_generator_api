from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.utils.data_handlers import UserDataHandler
from app.utils import decode_token
from .exceptions import AuthorizationException
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_email_from_token(token: str = Depends(oauth2_scheme)):
    authorization_exeption = AuthorizationException("invalid token")
    payload = decode_token(token)
    if payload is None:
        raise authorization_exeption
    username: str = payload.get("email")
    if username is None:
        raise authorization_exeption
    return username


def get_logged_user_instance(
    request: Request,
    user_email: str = Depends(get_email_from_token),
    db: Session = Depends(get_db),
):
    user_data_handler = UserDataHandler(db)
    user_instance = user_data_handler.get_user_by_email(user_email)
    if user_instance is None:
        raise AuthorizationException("user not found")
    if user_instance.is_active is False:
        raise AuthorizationException("user is inactive")

    # adding user instance and db session to request
    # be reusable in each needed endpoint
    request.state.user = user_instance
    request.state.db = db

    return user_instance
