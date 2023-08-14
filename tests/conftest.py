import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.database import SQLALCHEMY_DATABASE_URL, AsyncEngine, DatabaseSessionManager
from src.main import create_app


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def client() -> AsyncClient:
    app: FastAPI = create_app()
    sessionmanager = DatabaseSessionManager()
    sessionmanager.init(SQLALCHEMY_DATABASE_URL + '/postgres_test')

    engine: AsyncEngine = sessionmanager._engine

    async with engine.begin() as conn:
        await sessionmanager.drop_all(conn)
        await sessionmanager.create_all(conn)

    async with AsyncClient(app=app, base_url='http://127.0.0.1:5000') as c:
        yield c
