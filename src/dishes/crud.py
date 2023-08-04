from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Dish
from .schemas import DishCreate, DishUpdate
from src.dependencies import get_session


class DishRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session
        self.model = Dish

    async def get(self, dish_id: UUID4):
        stmt = select(self.model).where(self.model.id == dish_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_submenu_dishes(
        self, submenu_id: UUID4, skip: int = 0, limit: int = 100
    ):
        stmt = (
            select(self.model)
            .where(self.model.submenu_id == submenu_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, dish: DishUpdate, dish_id: UUID4):
        db_dish = await get_dish(dish_id)
        dish_data = dish.model_dump(exclude_unset=True)
        for key, value in dish_data.items():
            setattr(db_dish, key, value)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return db_dish

    async def delete(self, dish_id: UUID4):
        db_dish = await get_dish(dish_id)
        await self.session.delete(db_dish)
        await self.session.commit()

    async def create_submenu_dish(
        self, dish: DishCreate, submenu_id: UUID4
    ):
        db_dish = self.model(**dish.model_dump(), submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return db_dish
