from collections.abc import Mapping
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    random_username = f"user_{uuid.uuid4().hex[:6]}"
    random_email = f"{random_username}@email.com"
    response = client.post("/register", json = {
        "username": random_username,
        "email": random_email,
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == random_username
    assert data["email"] == random_email
    assert "id" in data

def  test_create_duplicate_user(test_user: Mapping[str, str]):

    # create user again with same credentials
    response = client.post("/register", json = {
        "username": test_user["username"],
        "email": test_user["email"],
        "password": "password123"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"