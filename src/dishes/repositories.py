from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRedisCacheRepository
from src.dependencies import get_session
from src.dishes.models import Dish
from src.dishes.schemas import DishCreate, DishUpdate


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session
        self.model = Dish

    async def get(self, dish_id: UUID4):
        stmt = select(self.model).where(self.model.id == dish_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self, submenu_id: UUID4, skip: int = 0, limit: int = 100):
        stmt = (
            select(self.model)
            .where(self.model.submenu_id == submenu_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, dish: DishUpdate, dish_id: UUID4):
        db_dish = await self.get(dish_id)
        dish_data = dish.model_dump(exclude_unset=True)
        for key, value in dish_data.items():
            setattr(db_dish, key, value)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return db_dish

    async def delete(self, dish_id: UUID4):
        db_dish = await self.get(dish_id)
        await self.session.delete(db_dish)
        await self.session.commit()

    async def create(self, dish: DishCreate, submenu_id: UUID4):
        db_dish = self.model(**dish.model_dump(), submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return db_dish


class DishCacheRepository(BaseRedisCacheRepository):
    ...
