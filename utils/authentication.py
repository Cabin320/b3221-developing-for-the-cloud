from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status

from utils.mongo_db_connect import connect_to_db
from utils.base_models import UserInDB, TokenData, UserLogin
from utils.env_vars import SECRET_KEY, ALGORITHM, CONNECTION_STRING, DB_NAME

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

client = connect_to_db(CONNECTION_STRING)
database = client[DB_NAME]


def verify_password(plain_password, hashed_password):
    """
    Verify the password entered by user
    :param plain_password:
    :param hashed_password:
    :return: Verified password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash the password entered by user
    :param password:
    :return: Hashed password
    """
    return pwd_context.hash(password)


def get_user(database, username: str):
    """
    Retrieve the user from the database
    :param database:
    :param username:
    :return: Username and Password
    """
    owners_collection = database["owners"]
    walkers_collection = database["walkers"]

    user_data = owners_collection.find_one({"user": username})
    if user_data:
        return UserInDB(username=user_data["user"], hashed_password=user_data["password"])

    user_data = walkers_collection.find_one({"user": username})
    if user_data:
        return UserInDB(username=user_data["user"], hashed_password=user_data["password"])

    return None


def authenticate_user(database, username: str, password: str):
    """
    Authenticate the username and password entered
    :param database:
    :param username:
    :param password:
    :return: Username and Password
    """
    user = get_user(database, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT
    :param data:
    :param expires_delta:
    :return: encoded JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Gets the current user
    :param token:
    :return: Validated user with access token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserLogin, Depends(get_current_user)]
):
    """
    Determines the current user logged in
    :param current_user:
    :return: Expires access token for current user if over 30 minutes logged in
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
