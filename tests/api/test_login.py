import secrets
from sqlmodel import Session
from pydantic import EmailStr
from fastapi.testclient import TestClient
from gilgates_api.model import User
from gilgates_api.services.auth.password import hash_password
from gilgates_api import dao_factory


async def test_login(client: TestClient, session: Session):
    dao = dao_factory(session)

    email = f"{secrets.token_hex(8)}@example.com"
    password = secrets.token_hex(10)

    user = User(name="Test user for test_login", email=EmailStr(email))
    user.password = hash_password(password)
    await dao.user.create(user)

    resp = client.post("/login", data={"username": email, "password": password})

    data = resp.json()
    assert resp.status_code == 200
    assert "access_token" in dict(data).keys()
    assert "refresh_token" in dict(data).keys()


async def test_login_with_signup(client: TestClient):
    name = "Test user for test_login_with_signup"
    email = f"{secrets.token_hex(8)}@example.com"
    password = secrets.token_hex(10)

    resp = client.post(
        "/signup", json={"name": name, "email": email, "password": password}
    )
    data = resp.json()
    assert resp.status_code == 200

    resp = client.post("/login", data={"username": email, "password": password})

    data = resp.json()
    assert resp.status_code == 200
    assert "access_token" in dict(data).keys()
    assert "refresh_token" in dict(data).keys()
