from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect_to_db(connection_str: str) -> MongoClient:
    """
    Connect to MongoDB and return MongoClient object
    :param connection_str:
    :return:
    """
    try:
        client = MongoClient(connection_str)
    except ConnectionFailure as e:
        raise f"Could not connect to MongoDB: {e}"
    return client
