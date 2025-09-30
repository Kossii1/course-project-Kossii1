from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_login():
    # Регистрация
    r = client.post("/auth/register", json={"username": "alice", "password": "123"})
    assert r.status_code == 200

    # Логин
    r = client.post("/auth/login", json={"username": "alice", "password": "123"})
    assert r.status_code == 200
