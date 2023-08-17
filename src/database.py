import contextlib
from typing import AsyncIterator

from redis import asyncio as aioredis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER, REDIS_HOST

redis = aioredis.from_url(f'redis://{REDIS_HOST}')

SQLALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
)
async_session = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


class Base(DeclarativeBase):
    metadata = MetaData()


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, SQLALCHEMY_DATABASE_URL: str) -> None:
        self._engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=True,
            future=True,
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initialized')
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initialized')

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception('DatabaseSessionManager is not initialized')

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


session_manager = DatabaseSessionManager()
session_manager.init(SQLALCHEMY_DATABASE_URL)
