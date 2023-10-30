from __future__ import annotations
from flask import current_app
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta

algorithm = "HS256"


def encode(**values: any) -> str:
    return jwt.encode(
        {
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=60),
            **values
        },
        current_app.secret_key,
        algorithm=algorithm
    )


def decode(token: str) -> dict[str, any]:
    return jwt.decode(
        token,
        current_app.secret_key,
        algorithms=[algorithm]
    )


def try_decode(token: str, default: dict[str, any] = {}) -> dict[str, any]:
    try:
        return decode(token)
    except InvalidTokenError:
        return default
