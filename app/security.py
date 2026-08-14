import datetime as dt
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.settings import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return password_hash.verify(password, hash)


ALGORITHM = "HS256"


def encode_access_token(
    subject: str,
    expiration_time: dt.timedelta = dt.timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    ),
) -> str:
    claims = {
        "sub": subject,
        "exp": dt.datetime.now(dt.UTC) + expiration_time,
    }

    return jwt.encode(
        payload=claims,
        key=settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    claims = jwt.decode(
        token,
        key=settings.JWT_SECRET_KEY.get_secret_value(),
        algorithms=[ALGORITHM],
    )

    return claims


DUMMY_HASH = hash_password("hunter2")
