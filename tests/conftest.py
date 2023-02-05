from datetime import timedelta
import secrets
import pytest
from pydantic import EmailStr
from sqlmodel import Session
from fastapi.testclient import TestClient
from gilgates_api import dao_factory
from gilgates_api.server import app
from gilgates_api.database import engine
from gilgates_api.model import User
from gilgates_api.services.auth.token import create_access_token


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session


@pytest.fixture
async def user(session: Session) -> User:
    email = EmailStr(f"{secrets.token_hex(8)}@example.com")
    user = User(name="Test User", email=email)

    dao = dao_factory(session)
    await dao.user.create(user)
    return user

@pytest.fixture
def token(user: User):
    return create_access_token(user, timedelta(days=1))
