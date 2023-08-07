from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRedisCacheRepository
from src.dependencies import get_session
from src.dishes.models import Dish
from src.submenus.models import Submenu
from src.submenus.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session
        self.model = Submenu

    async def get(self, submenu_id: UUID4):
        stmt = select(
            self.model.id,
            self.model.title,
            self.model.description,
            select(func.count(Dish.id))
            .where(Dish.submenu_id == submenu_id)
            .label('dishes_count'),
        ).where(self.model.id == submenu_id)
        result = await self.session.execute(stmt)

        return result.mappings().one_or_none()

    async def list(self, menu_id: UUID4, skip: int = 0, limit: int = 100):
        stmt = (
            select(self.model)
            .where(self.model.menu_id == menu_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, submenu: SubmenuCreate, menu_id: UUID4):
        db_submenu = self.model(**submenu.model_dump(), menu_id=menu_id)
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)
        return db_submenu

    async def update(self, submenu: SubmenuUpdate, submenu_id: UUID4):
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        result = await self.session.execute(stmt)
        db_submenu = result.scalar_one_or_none()
        submenu_data = submenu.model_dump(exclude_unset=True)
        for key, value in submenu_data.items():
            setattr(db_submenu, key, value)
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)
        return db_submenu

    async def delete(self, submenu_id: UUID4):
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        result = await self.session.execute(stmt)
        db_submenu = result.scalar_one_or_none()
        await self.session.delete(db_submenu)
        await self.session.commit()


class SubmenuCacheRepository(BaseRedisCacheRepository):
    ...
