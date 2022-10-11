from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.endpoints.test_configuration import USER_EMAIL, USER_PASSWORD, _add_user
from app.utils.data_handlers import UserDataHandler
from app.models import User
from app.schemas import ConfigurationCreate
from app.schemas import UserCreate


def test_create_user(
    db_session: Session,
):
    user = UserCreate(
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )
    user_data_handler = UserDataHandler(db_session)
    assert user_data_handler.create_user(user)


def test_get_user_by_email(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user_data_handler = UserDataHandler(db_session)

    assert user_data_handler.get_user_by_email(USER_EMAIL).id == 1


def test_valid_credentials_ok(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user_data_handler = UserDataHandler(db_session)

    assert user_data_handler.valid_credentials(USER_EMAIL, USER_PASSWORD) is True


def test_valid_credentials_wrong_credentials(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user_data_handler = UserDataHandler(db_session)

    assert (
        user_data_handler.valid_credentials("wrong_email@example.com", USER_PASSWORD)
        is False
    )
