import secrets
import pytest
from pydantic import EmailStr
from fastapi.testclient import TestClient
from gilgates_api import context
from gilgates_api.server import app
from gilgates_api.model.user import User


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def user() -> User:
    email = EmailStr(f"{secrets.token_hex(8)}@example.com")
    user = User(name="Test User", email=email)

    dao = context.get()
    await dao.user.create(user)
    return user
