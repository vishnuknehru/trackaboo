from __future__ import annotations

import os
from typing import Generator, Optional

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

# Decision: DATABASE_URL defaults to the SQLite file at project root (one level
# up from backend/). The path is resolved relative to this file's location so
# the app works from any working directory.
_raw_url = os.getenv("DATABASE_URL", "../trackaboo.db")
if not _raw_url.startswith("sqlite"):
    # Treat bare path as sqlite+pysqlite URL
    _db_path = os.path.join(os.path.dirname(__file__), "..", _raw_url)
    DATABASE_URL = f"sqlite:///{os.path.normpath(_db_path)}"
else:
    DATABASE_URL = _raw_url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn: object, _connection_record: object) -> None:
    """Enable FK enforcement and WAL mode on every new SQLite connection."""
    cursor = dbapi_conn.cursor()  # type: ignore[attr-defined]
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


def get_db() -> Generator[Session, None, None]:  # type: ignore[type-arg]
    """FastAPI dependency: yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables(bind_engine: Optional[Engine] = None) -> None:
    """Create all tables defined in models. Called during app lifespan startup."""
    from app.models import Category, Inflow, Outflow  # noqa: F401 — import to register models

    target = bind_engine or engine
    Base.metadata.create_all(bind=target)
