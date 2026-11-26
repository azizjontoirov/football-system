import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Parolni tasodifiy tuz (salt) bilan PBKDF2-SHA256 yordamida xeshlaydi."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}${dk.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Kiritilgan parolni bazadagi xesh bilan xavfsiz (constant-time) solishtiradi."""
    try:
        salt, stored_hash = hashed_password.split("$", maxsplit=1)
    except ValueError:
        return False
    dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return hmac.compare_digest(dk.hex(), stored_hash)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Foydalanuvchi ma'lumotlari asosida imzolangan JWT token yaratadi."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """JWT tokenni tekshiradi va ichidagi payload ma'lumotlarini qaytaradi."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        return None