import pytest
from fastapi.testclient import TestClient

from app import dependencies
from app.main import app
from tests.utils import assert_rfc7807_structure

# Клиент FastAPI
client = TestClient(app)


# === Фикстура для очистки RATE_LIMIT между тестами ===
@pytest.fixture(autouse=True)
def clear_rate_limit():
    dependencies.RATE_LIMIT.clear()
    yield
    dependencies.RATE_LIMIT.clear()


# === Тесты для регистрации ===
def test_successful_registration():
    """Проверка успешной регистрации"""
    response = client.post(
        "/auth/register",
        json={"username": "alice", "password": "123", "captcha_token": "dev"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Registration successful"


def test_rate_limit_registration():
    """Проверка лимита регистрации (не больше 5 за 10 минут)"""
    # 5 успешных регистраций
    for i in range(5):
        r = client.post(
            "/auth/register",
            json={"username": f"user{i}", "password": "pass", "captcha_token": "dev"},
            headers={"origin": "http://127.0.0.1:8000"},
        )
        assert r.status_code == 200

    # 6-я регистрация должна вернуть 429
    r = client.post(
        "/auth/register",
        json={"username": "overflow", "password": "pass", "captcha_token": "dev"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert r.status_code == 429
    data = r.json()
    assert_rfc7807_structure(data)
    assert "Too many registration attempts" in data["detail"]


def test_invalid_captcha():
    """Проверка отклонения при некорректном CAPTCHA токене"""
    response = client.post(
        "/auth/register",
        json={"username": "bob", "password": "123", "captcha_token": "invalid"},
        headers={"origin": "http://127.0.0.1:8000"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Invalid CAPTCHA" in data["detail"]


def test_invalid_origin():
    """Проверка отклонения при недопустимом origin"""
    response = client.post(
        "/auth/register",
        json={"username": "charlie", "password": "123", "captcha_token": "dev"},
        headers={"origin": "http://malicious.com"},
    )
    assert response.status_code == 400
    data = response.json()
    assert_rfc7807_structure(data)
    assert "Invalid request origin" in data["detail"]
