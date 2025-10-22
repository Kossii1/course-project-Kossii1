from fastapi.testclient import TestClient

from app.main import app
from tests.utils import assert_rfc7807_structure

client = TestClient(app)


def test_register_empty_password():
    response = client.post(
        "/auth/register",
        json={"username": "testuser_empty", "password": "", "captcha_token": "dev"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert data["detail"] == "Password cannot be empty"


def test_register_short_password():
    response = client.post(
        "/auth/register",
        json={"username": "testuser_short", "password": "123", "captcha_token": "dev"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must be at least 8 characters" in data["detail"]


def test_register_missing_number():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser_nonum",
            "password": "Password!",
            "captcha_token": "dev",
        },
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must contain at least one digit" in data["detail"]


def test_register_missing_uppercase_letter():
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser_nospec",
            "password": "password123",
            "captcha_token": "dev",
        },
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must contain at least one uppercase letter" in data["detail"]


def test_login_empty_password():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": ""},
    )
    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert any("password" in err.get("loc", []) for err in data["detail"])


def test_login_short_password():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "123"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must be at least 8 characters" in data["detail"]


def test_login_missing_number():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "Password!"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must contain at least one digit" in data["detail"]


def test_login_missing_uppercase_letter():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "password123"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Password must contain at least one uppercase letter" in data["detail"]
