from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session, session_manager

def get_db():
    db = async_session()

    try:
        yield db
    finally:
        db.close()

async def get_session() -> AsyncSession:
    async with session_manager.session() as session:
        yield session
        