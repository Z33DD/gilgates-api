import secrets
from typing import Dict
from sqlmodel import Session
from pydantic import EmailStr
from fastapi.testclient import TestClient
from gilgates_api.model import User
from gilgates_api.services.auth.password import hash_password
from gilgates_api import dao_factory


async def test_get_user_me(client: TestClient, session: Session):
    dao = dao_factory(session)

    email = f"{secrets.token_hex(8)}@example.com"
    password = secrets.token_hex(10)

    user = User(name="Test user for test_login", email=EmailStr(email))
    user.password = hash_password(password)
    await dao.user.create(user)
    dao.commit()

    resp = client.post("/login", data={"username": email, "password": password})

    data: Dict[str, str] = resp.json()
    detail = data.get("detail")
    assert resp.status_code == 200, f"Response: {detail}"
    assert "access_token" in dict(data).keys()
    assert "refresh_token" in dict(data).keys()

    access_token = data.get("access_token")

    resp = client.get("/user/me", headers={"Authentication": f"Bearer {access_token}"})
    data: Dict[str, str] = resp.json()

    detail = data.get("detail")
    assert resp.status_code == 200, f"Response: {detail}"
    assert data.get('uid') == user.uid, f"Response: {detail}"
