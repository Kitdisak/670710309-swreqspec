"""SQLAlchemy engine and session factories."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings, get_settings


def create_database_engine(settings: Settings | None = None) -> Engine:
    """Create an engine for the PostgreSQL URL required by CON-TECH-01."""
    active_settings = settings or get_settings()
    return create_engine(active_settings.database_url, future=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    # รองรับ CON-TECH-01 และการเตรียม session สำหรับ IF-HIS-01
    """Create sessions that can be used by the booking data layer."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db_session() -> Generator[Session, None, None]:
    # รองรับ CON-TECH-01 และการเข้าถึงข้อมูลผู้รับบริการตาม IF-HIS-01
    """Yield and close a database session for future API dependencies."""
    session = create_session_factory(create_database_engine())()
    try:
        yield session
    finally:
        session.close()