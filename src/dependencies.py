from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_manager


async def get_session() -> AsyncSession:
    async with session_manager.session() as session:
        yield session
