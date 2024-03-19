from os import getenv

CONNECTION_STRING = {
    "host": getenv("HOST"),
    "port": getenv("PORT"),
    "username": getenv("USERNAME"),
    "password": getenv("PASSWORD")
}

DB_NAME = getenv("DB_NAME")
COLLECTION_NAME = getenv("COLLECTION_NAME")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "johndoe": {
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$3QEfYTtfW8bvg5bfrvga2unJwnfxmgjjIV9vQQS0jgEH0NTkWGkqe",
        "disabled": False,
    }
}

assert CONNECTION_STRING is not None, "Connection string is not defined"
assert DB_NAME is not None, "DB_NAME is not defined"
assert COLLECTION_NAME is not None, "COLLECTION_NAME is not defined"
