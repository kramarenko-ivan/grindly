import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from collections.abc import Mapping

client = TestClient(app)

@pytest.fixture
def test_user() -> Mapping[str, str]:
    random_username = f"user_{uuid.uuid4().hex[:6]}"
    random_email = f"{random_username}@email.com"
    response = client.post("/register", json = {
        "username": random_username,
        "email": random_email,
        "password": "password123"
    })
    assert response.status_code == 200
    return response.json() # return new credentials of the user (id, username, email, password)