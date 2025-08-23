from collections.abc import Mapping
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_habit(test_user: Mapping[str, str]):
    # create a habit for existing user
    response = client.post("/habits", json={
        "title": "Read a book",
        "description": "Read 30 minutes daily",
        "user_id": test_user["id"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read a book"
    assert data["description"] == "Read 30 minutes daily"
    assert data["user_id"] == test_user["id"]
    assert "id" in data

def test_create_habit_no_user():
    # trying to create a habit with non-existed user_id
    response = client.post("/habits", json={
        "title": "Meditate",
        "description": "15 minutes daily",
        "user_id": 999 # non-existing user
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_habits(test_user: Mapping[str, str]):
    # creating a habit for check GET
    client.post("/habits", json={
        "title": "Exercise",
        "description": "Morning workout",
        "user_id": test_user["id"]
    })
    response = client.get(f"/habits?user_id={test_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert any(habit["title"] == "Exercise" for habit in data)

def test_update_habit(test_user: Mapping[str, str]):
    # creating a habit
    create_response = client.post("/habits", json={
        "title": "Drink water",
        "description": "2 liters daily",
        "user_id": test_user["id"]
    })
    habit_id = create_response.json()["id"]

    # updating a habit
    update_response = client.put(f"/habits/{habit_id}", json={
        "title": "Drink more water",
        "description": "2.1 liters daily"
    })

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Drink more water"
    assert updated["description"] == "2.1 liters daily"

def test_delete_habit(test_user: Mapping[str, str]):
    # creating a habit
    create_response = client.post('/habits', json={
        "title": "Walk",
        "description": "5000 steps",
        "user_id": test_user["id"]
    })
    habit_id = create_response.json()["id"]

    # deleting a habit
    delete_response = client.delete(f'/habits/{habit_id}')
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Habit deleted"

    # checking that habit is deleted
    get_response = client.get(f"/habits/{habit_id}?user_id={test_user['id']}")
    assert get_response.status_code == 404
