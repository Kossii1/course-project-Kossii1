from fastapi.testclient import TestClient

from app.main import app
from tests.utils import assert_rfc7807_structure

client = TestClient(app)


def test_invalid_captcha_rfc7807():
    response = client.post(
        "/auth/register",
        json={"username": "user123", "password": "pass", "captcha_token": "wrong"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Invalid CAPTCHA" in data["detail"]


def test_invalid_origin_rfc7807():
    response = client.post(
        "/auth/register",
        json={"username": "user123", "password": "pass", "captcha_token": "dev"},
        headers={"origin": "http://malicious.com"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Invalid request origin" in data["detail"]


def test_invalid_login_rfc7807():
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "wrong"},
    )
    assert response.status_code == 401
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Invalid username or password" in data["detail"]


def test_workout_not_found_rfc7807():
    # Нужно логиниться для авторизации
    r = client.post("/auth/login", data={"username": "alice", "password": "123"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/workouts/999999", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Workout not found" in data["detail"]
