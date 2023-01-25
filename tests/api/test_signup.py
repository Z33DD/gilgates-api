from fastapi.testclient import TestClient
import secrets


async def test_signup(client: TestClient):
    email = f"{secrets.token_hex(8)}@example.com"

    resp = client.post(
        "/signup", json={"email": email, "name": "Test user", "password": "12324affas"}
    )

    assert resp.status_code == 200
