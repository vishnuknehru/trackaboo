"""
Test fixtures.

Decision: use an in-memory SQLite DB for full isolation between test sessions.
Each test gets a clean database via the `db_session` fixture (function scope).
The FastAPI `get_db` dependency is overridden so the TestClient uses the same
in-memory engine as the test assertions.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Category, Inflow, Outflow  # noqa: F401 — register models


@pytest.fixture(scope="function")
def db_engine():
    """Create a fresh in-memory SQLite engine for each test function."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def set_pragmas(dbapi_conn, _record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
    """Provide a transactional test session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """FastAPI TestClient with `get_db` overridden to use in-memory session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # session closed by db_session fixture

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seed_category(db_session: Session) -> Category:
    """Insert a single 'outflow' category and return the ORM object."""
    cat = Category(
        name="Housing",
        type="outflow",
        color="#4CAF50",
        description="Rent and utilities",
        created_at="2026-03-01T00:00:00Z",
        updated_at="2026-03-01T00:00:00Z",
    )
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def seed_inflow_category(db_session: Session) -> Category:
    """Insert a single 'inflow' category."""
    cat = Category(
        name="Salary",
        type="inflow",
        color="#2196F3",
        description=None,
        created_at="2026-03-01T00:00:00Z",
        updated_at="2026-03-01T00:00:00Z",
    )
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat
