from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.configuration import Configuration
from app.models.user import User


def test_random_password_without_parameters(
    client: TestClient,
):
    response = client.get("/api/random-password/")
    assert response.status_code == 400


def test_random_password_without_lenght(
    client: TestClient,
):
    parameters = "?numbers=1"
    response = client.get("/api/random-password/" + parameters)
    assert response.status_code == 400


def test_random_password_ok(
    db_session: Session,
    client: TestClient,
):
    _add_configuration(db_session)
    parameters = "?lenght=20&numbers=1"
    response = client.get("/api/random-password/" + parameters)
    assert response.status_code == 200
    assert len(response.json()["random_password"]) == 20


def _add_user(db_session: Session) -> User:
    user = User(email="email@email.com", password="password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _add_configuration(db_session: Session) -> None:
    user = _add_user(db_session)
    config = Configuration(
        lenght=200,
        numbers=True,
        lowercase_chars=True,
        uppercase_chars=True,
        special_symbols=True,
        is_active=True,
        user_id=user.id,
    )
    db_session.add(config)
    db_session.commit()
    db_session.refresh(config)
