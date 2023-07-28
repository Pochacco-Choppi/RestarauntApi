from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Dish
from .schemas import DishCreate, DishUpdate


async def get_dish(session: AsyncSession, dish_id: UUID4):
    stmt = select(Dish).where(Dish.id == dish_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def list_submenu_dish(submenu_id: UUID4, session: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Dish).where(Dish.submenu_id == submenu_id).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_dish(session: AsyncSession, dish: DishUpdate, dish_id: UUID4):
    db_dish = await get_dish(session, dish_id)
    dish_data = dish.dict(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish

async def delete_dish(session: AsyncSession, dish_id: UUID4):
    db_dish = await get_dish(session, dish_id)
    await session.delete(db_dish)
    await session.commit()

async def create_submenu_dish(session: AsyncSession, dish: DishCreate, submenu_id: UUID4):
    db_dish = Dish(**dish.dict(), submenu_id=submenu_id)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish
