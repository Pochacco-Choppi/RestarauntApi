from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.submenus.models import Submenu
from src.dishes.models import Dish
from src.menus.models import Menu
from src.menus.schemas import MenuCreate, MenuUpdate

async def get_menu(session: AsyncSession, menu_id: UUID4):
    stmt = select(
        Menu.id,
        Menu.title,
        Menu.description,
        select(
            func.count(Submenu.id)
            ).where(Submenu.menu_id == menu_id).label("submenus_count"),
        select(
            func.count(Dish.id)
            ).join(
                Submenu
            ).where(
                and_(Submenu.menu_id == menu_id, Submenu.id == Dish.submenu_id)
            ).label("dishes_count"),
        ).where(
            Menu.id == menu_id
        ).select_from(
            Menu
        ).group_by(
            Menu.id
        )
    result = await session.execute(stmt)

    return result.mappings().one_or_none()

async def list_menu(session: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Menu).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_menu(session: AsyncSession, menu: MenuCreate):
    db_menu = Menu(title=menu.title, description=menu.description)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu

async def update_menu(session: AsyncSession, menu: MenuUpdate, menu_id: UUID4):
    stmt = select(Menu).where(Menu.id == menu_id)
    result = await session.execute(stmt)
    db_menu = result.scalar_one_or_none()
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu

async def delete_menu(session: AsyncSession, menu_id: UUID4):
    stmt = select(Menu).where(Menu.id == menu_id)
    result = await session.execute(stmt)
    db_menu = result.scalar_one_or_none()
    await session.delete(db_menu)
    await session.commit()
