import os


def get_db_connection_string() -> str:
    result = os.getenv("DB_URI")
    if result is None:
        raise ValueError()
    return result
