from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

from src.infrastructure.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Set to True for SQLAlchemy to echo queries
    pool_pre_ping=True,   # Enables the connection pool "pre-ping" feature
)

# Create async session factory
async_session_factory = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Create a base class for declarative models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an async database session with automatic commit/rollback handling.
    
    Returns:
        AsyncGenerator yielding an AsyncSession
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    """Initialize the database with tables."""
    async with engine.begin() as conn:
        # Drop all tables if they exist to start fresh (for demo purposes)
        # Remove this line in production!
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
