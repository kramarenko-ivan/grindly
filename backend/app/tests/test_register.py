from app.tests.conftest import TestFactory
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user(factory: TestFactory):
    user = factory.create_user()
    assert "id" in user
    assert "username" in user
    assert "email" in user


def test_create_duplicate_user(factory: TestFactory):
    user = factory.create_user()
    response = client.post(
        "/register",
        json={
            "username": user["username"],
            "email": user["email"],
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"
