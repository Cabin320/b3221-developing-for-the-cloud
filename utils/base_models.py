from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Dog(BaseModel):
    name: list[str]
    breed: list[str]
    age: list[str]


class User(BaseModel):
    user: str
    email: str
    location: str
    password: str
    dog: Optional[Dog] = None
