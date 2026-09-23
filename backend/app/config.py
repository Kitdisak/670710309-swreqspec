"""Configuration for the booking backend."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings required to connect to the configured database."""

    database_url: str


def get_settings() -> Settings:
    """Read the database URL required by CON-TECH-01 from the environment."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be configured")
    return Settings(database_url=database_url)