from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.dishes.models import Dish
from src.submenus.models import Submenu
from src.submenus.schemas import SubmenuCreate, SubmenuUpdate


async def get_submenu(session: AsyncSession, submenu_id: UUID4):
    stmt = select(
        Submenu.id,
        Submenu.title,
        Submenu.description,
        select(func.count(Dish.id))
        .where(Dish.submenu_id == submenu_id)
        .label("dishes_count"),
    ).where(Submenu.id == submenu_id)
    result = await session.execute(stmt)

    return result.mappings().one_or_none()


async def list_menu_submenu(
    menu_id: UUID4, session: AsyncSession, skip: int = 0, limit: int = 100
):
    stmt = select(Submenu).where(Submenu.menu_id == menu_id).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_menu_submenu(
    session: AsyncSession, submenu: SubmenuCreate, menu_id: UUID4
):
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


async def update_submenu(
    session: AsyncSession, submenu: SubmenuUpdate, submenu_id: UUID4
):
    stmt = select(Submenu).where(Submenu.id == submenu_id)
    result = await session.execute(stmt)
    db_submenu = result.scalar_one_or_none()
    submenu_data = submenu.model_dump(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


async def delete_submenu(session: AsyncSession, submenu_id: UUID4):
    stmt = select(Submenu).where(Submenu.id == submenu_id)
    result = await session.execute(stmt)
    db_submenu = result.scalar_one_or_none()
    await session.delete(db_submenu)
    await session.commit()
