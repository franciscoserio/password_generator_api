from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.endpoints.test_configuration import _add_user
from app.utils.data_handlers import ConfigurationDataHandler
from app.models import User
from app.schemas import ConfigurationCreate


def test_create_configuration(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user = db_session.query(User).first()
    config = ConfigurationCreate(
        lenght=123,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        is_active=True,
    )
    configuration_data_handler = ConfigurationDataHandler(db_session, user)
    assert configuration_data_handler.create_configuration(config)


def test_get_config_by_id_ok(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user = db_session.query(User).first()
    config = ConfigurationCreate(
        lenght=123,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        is_active=True,
    )
    configuration_data_handler = ConfigurationDataHandler(db_session, user)
    configuration_data_handler.create_configuration(config)

    assert configuration_data_handler.get_config_by_id(1).lenght == 123


def test_get_config_by_id_inexistent_config(
    db_session: Session,
    client: TestClient,
):
    _add_user(client)
    user = db_session.query(User).first()
    config = ConfigurationCreate(
        lenght=123,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        is_active=True,
    )
    configuration_data_handler = ConfigurationDataHandler(db_session, user)

    assert configuration_data_handler.get_config_by_id(1) is None
