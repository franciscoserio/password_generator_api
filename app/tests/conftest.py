from typing import Any, Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils import get_db
from app.main import app
from app.utils.database import Base


# Set sqlite as database for running tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def application() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case
    """
    Base.metadata.create_all(engine)
    _app = app
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(application: FastAPI) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(
    application: FastAPI, db_session: Session
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    application.dependency_overrides[get_db] = _get_test_db
    with TestClient(application) as client:
        yield client
