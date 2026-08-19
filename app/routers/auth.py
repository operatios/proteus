from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from app import security
from app.deps import get_user_service
from app.exceptions import UserAlreadyExists
from app.models import User
from app.schemas.auth import RegisterIn, RegisterOut, Token, UserOut
from app.services.user_service import UserService

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    user_service: UserServiceDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
    except jwt.InvalidTokenError:
        raise credentials_exception

    if not payload.get("sub"):
        raise credentials_exception

    user = await user_service.get_by_username(payload["sub"])
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login(
    user_service: UserServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await user_service.authenticate_credentials(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.encode_access_token(user.username)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_service: UserServiceDep,
    data: RegisterIn,
) -> RegisterOut:
    try:
        user = await user_service.create(**data.model_dump())
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return RegisterOut.model_validate(user, from_attributes=True)


@router.get("/me")
async def get_me(user: Annotated[User, Depends(get_current_user)]) -> UserOut:
    return UserOut.model_validate(user, from_attributes=True)
