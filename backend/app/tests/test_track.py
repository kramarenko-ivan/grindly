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


def test_get_tracks_for_user(
    test_user: Mapping[str, str],
    habit_factory: Callable[[int, str], Dict[str, str]],
    track_factory: Callable[[int, int], Dict[str, str]],
):
    habit1 = habit_factory(int(test_user["id"]), "Reading")
    habit2 = habit_factory(int(test_user["id"]), "Running")

    track_factory(int(test_user["id"]), int(habit1["id"]))
    track_factory(int(test_user["id"]), int(habit2["id"]))

    response = client.get(f"/track?user_id={test_user['id']}")

    assert response.status_code == 200

    tracks = response.json()
    habit_ids = [t["habit_id"] for t in tracks]

    assert habit1["id"] in habit_ids
    assert habit2["id"] in habit_ids


def test_get_tracks_for_habit(
    test_user: Mapping[str, str],
    habit_factory: Callable[[int, str], Dict[str, str]],
    track_factory: Callable[[int, int], Dict[str, str]],
):
    habit = habit_factory(int(test_user["id"]), "Pushups")

    track_factory(int(test_user["id"]), int(habit["id"]))
    track_factory(int(test_user["id"]), int(habit["id"]))

    response = client.get(f"/track?user_id={test_user['id']}&habit_id={habit['id']}")
    assert response.status_code == 200

    tracks = response.json()
    assert all(t["habit_id"] == habit["id"] for t in tracks)
    assert len(tracks) >= 2


def test_delete_track(
    test_user: Mapping[str, str],
    habit_factory: Callable[[int, str], Dict[str, str]],
    track_factory: Callable[[int, int], Dict[str, str]],
):
    habit = habit_factory(int(test_user["id"]), "Yoga")
    track = track_factory(int(test_user["id"]), int(habit["id"]))
    track_id = track["id"]

    delete_response = client.delete(f"/track/{track_id}?user_id={test_user["id"]}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Track deleted"

    get_response = client.get(f"/track/{track_id}?user_id={test_user['id']}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Track not found"


def test_delete_nonexistent_track(test_user: Mapping[str, str]):
    response = client.delete(f"/track/9999?user_id={test_user['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Track not found"
