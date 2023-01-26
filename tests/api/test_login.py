from pydantic import EmailStr
from fastapi.testclient import TestClient
import secrets
from gilgates_api.model.user import User
from gilgates_api import context
from gilgates_api.services.auth.password import hash_password


async def test_login(client: TestClient):
    dao = context.get()
    
    email = f"{secrets.token_hex(8)}@example.com"
    password = secrets.token_hex(10)
    
    user = User(name="Pedro Antonio", email=EmailStr(email))
    user.password = hash_password(password)
    await dao.user.create(user)

    resp = client.post(
        "/login", data={
            "username": email,
            "password": password
        }
    )

    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in dict(data).keys()
    assert "refresh_token" in dict(data).keys()
