"""Shared database fixtures for backend tests."""

import os
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.config import get_settings
from app.db.session import create_session_factory


@pytest.fixture
def database_url(monkeypatch: pytest.MonkeyPatch) -> str:
    # รองรับ CON-TECH-01 โดยแยกฐานข้อมูลทดสอบจาก PostgreSQL ของระบบจริง
    """Configure SQLite for tests while production reads DATABASE_URL."""
    url = "sqlite+pysqlite:///:memory:"
    monkeypatch.setenv("DATABASE_URL", url)
    return url


@pytest.fixture
def database_engine(database_url: str) -> Generator[Engine, None, None]:
    # รองรับ CON-TECH-01 และเตรียม session สำหรับข้อมูลตาม IF-HIS-01
    """Create a shared in-memory SQLite engine for one test."""
    engine = create_engine(
        get_settings().database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(database_engine: Engine) -> Generator[Session, None, None]:
    # รองรับ CON-TECH-01 และการเตรียม session สำหรับ IF-HIS-01
    """Provide a transaction-ready SQLAlchemy session for backend tests."""
    session = create_session_factory(database_engine)()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_database_session_fixture(db_session: Session, database_url: str) -> None:
    """Verify T-01 can read DATABASE_URL and create a SQLite session."""
    assert os.environ["DATABASE_URL"] == database_url
    assert db_session.bind is not None
    assert db_session.bind.url.database == ":memory:"