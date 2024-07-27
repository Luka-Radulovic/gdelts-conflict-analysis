import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session


def get_db_connection_string() -> str:
    result = os.getenv("DB_URI")
    if result is None:
        sqlite_db_path = "test_database.sqlite"

        if not os.path.exists(sqlite_db_path):
            conn = sqlite3.connect(sqlite_db_path)
            conn.close()

        result = f"sqlite:///{sqlite_db_path}"
    return result


engine = create_engine(get_db_connection_string())


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
