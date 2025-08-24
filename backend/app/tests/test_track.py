from collections.abc import Mapping
from typing import Callable, Dict
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_track(
    test_user: Mapping[str, str],
    habit_factory: Callable[[int, str], Dict[str, str]],
    track_factory: Callable[[int, int], Dict[str, str]],
):
    habit = habit_factory(int(test_user["id"]), "Jogging")
    track = track_factory(int(test_user["id"]), int(habit["id"]))

    assert track["habit_id"] == habit["id"]
    assert track["user_id"] == test_user["id"]
    assert "timestamp" in track


def test_create_track_wrong_user(
    test_user: Mapping[str, str], habit_factory: Callable[[int, str], Dict[str, str]]
):
    habit = habit_factory(int(test_user["id"]), "Meditation")

    response = client.post(
        "/track", params={"user_id": 999}, json={"habit_id": habit["id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found for this user"
