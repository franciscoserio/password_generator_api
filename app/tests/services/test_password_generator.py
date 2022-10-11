from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.endpoints.test_configuration import _add_configuration
from app.services import PasswordGeneratorService
from app.utils.data_handlers import ConfigurationDataHandler


def test_validate_params(
    db_session: Session,
):
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=200,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    assert password_generator_service._validate_params() is None


def test_get_char_types_ok(
    db_session: Session,
    client: TestClient,
):
    _ = _add_configuration(client)
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=200,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    assert len(password_generator_service._get_char_types()) == 4


def test_get_char_types_one_flag_false(
    db_session: Session,
    client: TestClient,
):
    _ = _add_configuration(client)
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=200,
        numbers=True,
        lowercase_chars=False,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    assert len(password_generator_service._get_char_types()) == 3


def test_get_char_types_one_missing_flag(
    db_session: Session,
    client: TestClient,
):
    _ = _add_configuration(client)
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=200,
        numbers=True,
        lowercase_chars=None,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    assert len(password_generator_service._get_char_types()) == 4


def test_generate_password_ok(
    db_session: Session,
    client: TestClient,
):
    _ = _add_configuration(client)
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=123,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    password_generator_service._generate_password()
    assert len(password_generator_service.password) == 123


def test_generate_password_without_lenght(
    db_session: Session,
    client: TestClient,
):
    _ = _add_configuration(client)
    configuration_data_handler = ConfigurationDataHandler(db_session)
    password_generator_service = PasswordGeneratorService(
        lenght=None,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        configuration_data_handler=configuration_data_handler,
    )
    password_generator_service._generate_password()
    assert len(password_generator_service.password) == 10
