import pytest
from fastapi.testclient import TestClient
from gilgates_api.server import app


@pytest.fixture
def client():
    return TestClient(app)
