from typing import Dict
from fastapi.testclient import TestClient
from gilgates_api.model import User


async def test_get_user_me(client: TestClient, user: User, token: str):
    resp = client.get("/user/me", headers={"Authentication": f"Bearer {token}"})
    data: Dict[str, str] = resp.json()

    detail = data.get("detail")
    assert resp.status_code == 200, f"Response: {detail}"
    assert data.get('uid') == user.uid, f"Response: {detail}"

async def test_get_users(client: TestClient, token: str):
    resp = client.get("/user/me", headers={"Authentication": f"Bearer {token}"})
    data: Dict[str, str] = resp.json()

    detail = data.get("detail")
    assert resp.status_code == 200, f"Response: {detail}"
