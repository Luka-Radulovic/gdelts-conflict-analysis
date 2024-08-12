from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine, create_engine  # type: ignore
from sqlalchemy.orm.session import Session

from gdelt_api.database import get_db_connection_string


class Database:
    engine: Engine | None = None  # type: ignore

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        self.engine = self.engine or create_engine(get_db_connection_string())
        session = Session(self.engine, expire_on_commit=False)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


db = Database()
session_scope = db.session_scope
