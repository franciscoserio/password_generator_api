from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services import AuthenticationService
from app.utils.data_handlers import UserDataHandler
from app.tests.endpoints.test_configuration import USER_EMAIL, USER_PASSWORD, _add_user


def test_validate_credentials_ok(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user_data_handler = UserDataHandler(db_session)
    authentication_service = AuthenticationService(
        email=USER_EMAIL,
        password=USER_PASSWORD,
        user_data_handler=user_data_handler,
    )
    assert authentication_service._validate_credentials() == True


def test_validate_credentials_invalid_credentials(
    db_session: Session,
):
    user_data_handler = UserDataHandler(db_session)
    authentication_service = AuthenticationService(
        email=USER_EMAIL,
        password=USER_PASSWORD,
        user_data_handler=user_data_handler,
    )
    assert authentication_service._validate_credentials() == False


def test_get_access_token(
    db_session: Session,
):
    user_data_handler = UserDataHandler(db_session)
    authentication_service = AuthenticationService(
        email=USER_EMAIL,
        password=USER_PASSWORD,
        user_data_handler=user_data_handler,
    )
    assert authentication_service._get_access_token()
