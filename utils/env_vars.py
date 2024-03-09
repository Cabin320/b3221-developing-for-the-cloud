from os import getenv

CONNECTION_STRING = {
    "host": getenv("HOST"),
    "port": getenv("PORT"),
    "username": getenv("USERNAME"),
    "password": getenv("PASSWORD")
}

DB_NAME = getenv("DB_NAME")
COLLECTION_NAME = getenv("COLLECTION_NAME")
