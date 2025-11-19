import os

import requests
from dotenv import load_dotenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
load_dotenv()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


def verify_captcha(token: str) -> bool:
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": RECAPTCHA_SECRET_KEY, "response": token},
    )
    result = response.json()
    return result.get("success", False)
