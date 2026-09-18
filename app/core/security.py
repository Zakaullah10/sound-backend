import bcrypt

from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


# JWT settings
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
DEFAULT_REFRESH_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60


def create_access_token(
    data: dict,
    expire_minutes: int | None = None,
) -> tuple[str, datetime]:
    to_encode = {
        key: value
        for key, value in data.items()
        if key not in {"exp", "type", "access_expire_minutes", "refresh_expire_minutes"}
    }

    minutes = (
        expire_minutes
        if expire_minutes is not None
        else ACCESS_TOKEN_EXPIRE_MINUTES
    )

    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode["exp"] = expire

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire


def create_refresh_token(
    data: dict,
    expire_minutes: int | None = None,
) -> tuple[str, datetime]:
    to_encode = {
        key: value
        for key, value in data.items()
        if key not in {"exp", "type"}
    }

    minutes = (
        expire_minutes
        if expire_minutes is not None
        else DEFAULT_REFRESH_EXPIRE_MINUTES
    )

    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expire
