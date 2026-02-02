"""
Database Session Management.

Handles async database connection and session creation.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    create_async_engine, 
    async_sessionmaker,
    AsyncEngine
)

from src.infrastructure.config import get_settings
from src.infrastructure.db.models import Base

# Global engine and session factory
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker | None = None


def get_db_url() -> str:
    """Get Database URL from settings."""
    settings = get_settings()
    # If explicit DB URL is set in settings (env var), use it.
    # Otherwise default to sqlite async.
    # Note: Settings might not have it yet, so fallback to env or default.
    return getattr(settings, "database_url", "sqlite+aiosqlite:///./maestro.db")


def get_engine() -> AsyncEngine:
    """Get or create Async Engine."""
    global _engine
    if _engine is None:
        db_url = get_db_url()
        _engine = create_async_engine(
            db_url,
            echo=False, # Set to True for SQL logging
            future=True
        )
    return _engine


def get_session_factory() -> async_sessionmaker:
    """Get or create Session Factory."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        _session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )
    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async Context Manager for Database Session.
    
    Usage:
        async with get_session() as session:
            await session.execute(...)
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database (create tables)."""
    engine = get_engine()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Uncomment to reset
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connection."""
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None
