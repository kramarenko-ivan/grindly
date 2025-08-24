from app.tests.conftest import TestFactory
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_habit(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(
        int(user["id"]),
        "Read a book",
        "Read 30 minutes daily",
    )

    assert habit["title"] == "Read a book"
    assert habit["description"] == "Read 30 minutes daily"
    assert habit["user_id"] == user["id"]
    assert "id" in habit


def test_create_habit_no_user(factory: TestFactory):
    response = client.post(
        "/habits",
        json={
            "title": "Meditate",
            "description": "15 minutes daily",
            "user_id": 999,
        },  # non-existing user
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_habits(factory: TestFactory):
    user = factory.create_user()
    factory.create_habit(int(user["id"]), "Exercise", "Morning workout")

    response = client.get(f"/habits?user_id={user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert any(habit["title"] == "Exercise" for habit in data)


def test_update_habit(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Drink water", "2 liters daily")

    update_response = client.put(
        f"/habits/{habit['id']}",
        json={"title": "Drink more water", "description": "2.1 liters daily"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Drink more water"
    assert updated["description"] == "2.1 liters daily"


def test_delete_habit(factory: TestFactory):
    user = factory.create_user()
    habit = factory.create_habit(int(user["id"]), "Walk", "5000 steps")

    delete_response = client.delete(f"/habits/{habit["id"]}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Habit deleted"

    get_response = client.get(f"/habits/{habit["id"]}?user_id={int(user['id'])}")
    assert get_response.status_code == 404
