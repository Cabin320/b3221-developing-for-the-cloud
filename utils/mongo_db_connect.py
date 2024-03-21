import backoff
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


@backoff.on_exception(
    backoff.expo,
    ConnectionFailure,
    max_tries=3
)
def connect_to_db(connection_str: str) -> MongoClient:
    """
    Connect to MongoDB and return MongoClient object
    :param connection_str:
    :return: MongoClient object
    """
    try:
        client = MongoClient(connection_str)
        print(client.server_info())
    except ConnectionFailure as e:
        raise f"Could not connect to MongoDB: {e}"
    return client
