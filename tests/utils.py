import re


def assert_rfc7807_structure(data: dict):
    """Проверяет структуру ответа RFC7807"""
    required_fields = ["type", "title", "status", "detail", "correlation_id"]
    for field in required_fields:
        assert field in data
    # Проверка, что correlation_id — UUID
    assert re.match(r"^[0-9a-fA-F-]{36}$", data["correlation_id"])
