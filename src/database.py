import contextlib
import os
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

db_user = os.environ['DATABASE_USER']
db_password = os.environ['DATABASE_PASSWORD']
db_host = os.environ['DATABASE_HOST']
db_port = os.environ['DATABASE_PORT']

redis_host = os.environ['REDIS_HOST']

redis = aioredis.from_url(f'redis://{redis_host}')

SQLALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}'
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
