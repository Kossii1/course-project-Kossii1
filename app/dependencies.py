import re
import time

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import auth, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


RATE_LIMIT = {}
LIMIT = 5
PERIOD = 600


def rate_limit_register(request: Request):
    ip = request.client.host
    now = time.time()

    attempts = RATE_LIMIT.get(ip, [])

    attempts = [t for t in attempts if now - t < PERIOD]

    if len(attempts) >= LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many registration attempts. Please try again later.",
        )

    attempts.append(now)
    RATE_LIMIT[ip] = attempts


ALLOWED_ORIGINS = ["http://127.0.0.1:8000"]


def validate_request_origin(request: Request):
    origin = request.headers.get("origin") or request.headers.get("referer")
    if not origin or not any(origin.startswith(allowed) for allowed in ALLOWED_ORIGINS):
        raise HTTPException(status_code=400, detail="Invalid request origin")


def validate_password(password: str):
    """Простая серверная валидация пароля. Бросает HTTPException с текстом ошибки."""
    if password is None or password == "":
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters"
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter",
        )
    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one digit"
        )
