import datetime as dt
from typing import Any

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.settings import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
    # await run_in_threadpool()
    return password_hash.verify(password, hash)


def authenticate(username: str, password: str) -> None:
    # user = UserService(session).get(username)
    # if user:
    # verify_password(password, user.hashed_password)
    # else:
    # verify_password(password, DUMMY_HASH)

    # return user
    return None


DUMMY_HASH = hash_password("hunter2")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    subject: str,
    expiration_time: dt.timedelta = dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    claims = {
        "sub": subject,
        "exp": dt.datetime.now(dt.UTC) + expiration_time,
    }

    return jwt.encode(
        payload=claims,
        key=settings.jwt_secret_key.get_secret_value(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        claims = jwt.decode(
            token,
            key=settings.jwt_secret_key.get_secret_value(),
            algorithms=[ALGORITHM],
        )
    except InvalidTokenError:
        raise  # TODO

    return claims
