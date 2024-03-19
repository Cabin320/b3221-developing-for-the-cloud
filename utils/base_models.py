from typing import List, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    email: str
    disabled: bool | None = None


class UserInDB(User):
    email: str
    hashed_password: str


class DogWalkerInfo(BaseModel):
    email: str
    password: str


class AdditionalPetInfo(BaseModel):
    name: str
    breed: str
    age: int


class DogOwnerInfo(BaseModel):
    email: str
    password: str
    dog: str
    breed: str
    age: int
    add_pet: Optional[List[AdditionalPetInfo]] = None
