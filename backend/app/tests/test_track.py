from app.tests.conftest import TestFactory
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_track(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Jogging")
    track = factory.create_track(int(user["id"]), int(habit["id"]))

    assert track["habit_id"] == habit["id"]
    assert track["user_id"] == user["id"]
    assert "timestamp" in track


def test_create_track_wrong_user(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Meditation")

    response = client.post(
        "/track", params={"user_id": 999}, json={"habit_id": habit["id"]}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found for this user"


def test_get_tracks_for_user(factory: TestFactory):
    user = factory.create_user()

    habit1 = factory.create_habit(int(user["id"]), "Reading")
    habit2 = factory.create_habit(int(user["id"]), "Running")

    factory.create_track(int(user["id"]), habit1["id"])
    factory.create_track(int(user["id"]), habit2["id"])

    response = client.get(f"/track?user_id={user['id']}")
    assert response.status_code == 200

    tracks = response.json()
    habit_ids = [t["habit_id"] for t in tracks]

    assert habit1["id"] in habit_ids
    assert habit2["id"] in habit_ids


def test_get_tracks_for_habit(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Pushups")

    factory.create_track(int(user["id"]), habit["id"])
    factory.create_track(int(user["id"]), habit["id"])

    response = client.get(f"/track?user_id={user['id']}&habit_id={habit['id']}")
    assert response.status_code == 200

    tracks = response.json()
    assert all(t["habit_id"] == habit["id"] for t in tracks)
    assert len(tracks) >= 2


def test_delete_track(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Yoga")
    track = factory.create_track(int(user["id"]), habit["id"])

    delete_response = client.delete(f"/track/{track['id']}?user_id={user['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Track deleted"

    get_response = client.get(f"/track/{track['id']}?user_id={user['id']}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Track not found"


def test_delete_nonexistent_track(factory: TestFactory):
    user = factory.create_user()
    response = client.delete(f"/track/9999?user_id={user['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Track not found"
