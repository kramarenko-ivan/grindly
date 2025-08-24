import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from collections.abc import Mapping

client = TestClient(app)


class TestFactory:
    # Factory for creating an objects of users, habits and tracks

    @staticmethod
    def create_user() -> Mapping[str, str]:
        random_username = f"user_{uuid.uuid4().hex[:6]}"
        random_email = f"{random_username}@email.com"
        response = client.post(
            "/register",
            json={
                "username": random_username,
                "email": random_email,
                "password": "password123",
            },
        )
        assert response.status_code == 200
        return response.json()

    @staticmethod
    def create_habit(
        user_id: int, title: str = "Simple Habit", description: str = "Make a something"
    ):
        response = client.post(
            "/habits",
            json={"title": title, "description": description, "user_id": user_id},
        )
        assert response.status_code == 200
        return response.json()

    @staticmethod
    def create_track(user_id: int, habit_id: int):
        response = client.post(
            "/track", params={"user_id": user_id}, json={"habit_id": habit_id}
        )
        assert response.status_code == 200
        return response.json()


@pytest.fixture
def factory():
    return TestFactory()
