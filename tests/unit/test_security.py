import base64
import json
from datetime import timedelta

import jwt
import pytest
from jwt import ExpiredSignatureError, InvalidTokenError

from app.security import (
    decode_access_token,
    encode_access_token,
    hash_password,
    verify_password,
)


@pytest.fixture
def password() -> str:
    return "hunter2"


def test_hash_password_not_equals_plaintext(password: str) -> None:
    assert hash_password(password) != password


def test_hash_password_is_salted(password: str) -> None:
    assert hash_password(password) != hash_password(password)


def test_verify_password_success(password: str) -> None:
    assert verify_password(password, hash_password(password))


def test_verify_password_failure(password: str) -> None:
    assert not verify_password("qwerty", hash_password(password))


@pytest.fixture
def subject() -> str:
    return "admin"


def test_encode_access_token(subject: str) -> None:
    token = encode_access_token(subject)
    assert token.startswith("ey")


def test_encode_and_decode_acess_token(subject: str) -> None:
    token = encode_access_token(subject)
    data = decode_access_token(token)
    assert data.get("sub") == subject


def test_decode_access_token_rejects_empty_string() -> None:
    with pytest.raises(InvalidTokenError):
        decode_access_token("")


def test_decode_access_token_rejects_tampered_payload(subject: str) -> None:
    token = encode_access_token(subject)
    header_b64, payload_b64, signature_b64 = token.split(".")

    # "==" is added for padding
    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "=="))
    payload["sub"] = "root"
    # We strip it afterwards since JWT tokens don't have padding
    tampered_payload_b64 = (
        base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    )

    tampered_token = f"{header_b64}.{tampered_payload_b64}.{signature_b64}"

    decoded_tampered_token = jwt.decode(
        tampered_token, options={"verify_signature": False}
    )
    assert decoded_tampered_token.get("sub") == "root"

    with pytest.raises(InvalidTokenError):
        decode_access_token(tampered_token)


@pytest.mark.parametrize(
    "expiration_time",
    [timedelta(seconds=0), timedelta(days=-1)],
)
def test_decode_access_token_rejects_expired_token(
    subject: str, expiration_time: timedelta
) -> None:
    token = encode_access_token(subject, expiration_time=expiration_time)
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)
