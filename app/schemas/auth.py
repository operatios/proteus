from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str = Field(min_length=1, max_length=32, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr


class UserOut(User):
    id: int


class RegisterIn(User):
    password: str


class RegisterOut(User):
    id: int
