from os import getenv

CONNECTION_STRING = getenv("CONNECTION_STRING")

DB_NAME = getenv("DB_NAME")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

assert CONNECTION_STRING is not None, "Connection string is not defined"
assert DB_NAME is not None, "DB_NAME is not defined"
assert SECRET_KEY is not None, "SECRET_KEY is not defined"
