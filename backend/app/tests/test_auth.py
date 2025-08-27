import os
from app.tests.conftest import TestFactory, client
from jose import jwt


def test_login_success(factory: TestFactory):
    user = factory.create_user()

    response = client.post(
        "/login",
        data={
            "username": user["username"],
            "password": "password123",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Check that token is valid and has user id
    decoded = jwt.decode(
        data["access_token"],
        os.getenv("SECRET_KEY", "defaultsecret"),
        algorithms=[os.getenv("ALGORITHM", "HS256")],
    )
    assert str(user["id"]) == decoded.get("sub")


def test_login_invalid_password(factory: TestFactory):
    user = factory.create_user()
    response = client.post(
        "/login", data={"username": user["username"], "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_nonexistent_user():
    response = client.post(
        "/login", data={"username": "nonexistent", "password": "password123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
