from fastapi.testclient import TestClient

from app.main import app
from tests.utils import assert_rfc7807_structure

client = TestClient(app)


def test_workouts():
    # Логин
    r = client.post("/auth/login", data={"username": "alice", "password": "123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # CREATE
    r = client.post(
        "/workouts", json={"date": "2025-09-29", "note": "Leg day"}, headers=headers
    )
    assert r.status_code == 200
    workout_id = r.json()["id"]

    # READ ONE
    r = client.get(f"/workouts/{workout_id}", headers=headers)
    assert r.status_code == 200

    # UPDATE
    r = client.patch(
        f"/workouts/{workout_id}", json={"note": "Chest day"}, headers=headers
    )
    assert r.status_code == 200
    assert r.json()["note"] == "Chest day"

    # DELETE
    r = client.delete(f"/workouts/{workout_id}", headers=headers)
    assert r.status_code == 200

    # Попытка получить workout чужого пользователя
    headers_wrong = {"Authorization": "Bearer INVALID_TOKEN"}
    r = client.get(f"/workouts/{workout_id}", headers=headers_wrong)
    assert r.status_code == 401
    data = r.json()
    assert_rfc7807_structure(data)

    # Попытка обновить несуществующий workout
    r = client.patch("/workouts/999999", json={"note": "Test"}, headers=headers)
    assert r.status_code == 404
    data = r.json()
    assert_rfc7807_structure(data)
