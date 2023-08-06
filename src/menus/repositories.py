from fastapi import Depends

import os

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from src.submenus.models import Submenu
from src.dishes.models import Dish
from src.menus.models import Menu
from src.menus.schemas import MenuCreate, MenuUpdate
from src.dependencies import get_session
from src.base.repositories import BaseRedisCacheRepository


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session: AsyncSession = session
        self.model = Menu

    async def get(self, menu_id: UUID4):
        stmt = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                select(func.count(Submenu.id))
                .where(Submenu.menu_id == menu_id)
                .label("submenus_count"),
                select(func.count(Dish.id))
                .join(Submenu)
                .where(and_(Submenu.menu_id == menu_id, Submenu.id == Dish.submenu_id))
                .label("dishes_count"),
            )
            .where(self.model.id == menu_id)
            .select_from(self.model)
            .group_by(self.model.id)
        )
        result = await self.session.execute(stmt)

        return result.mappings().one_or_none()

    async def list(self, skip: int = 0, limit: int = 100):
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, menu: MenuCreate):
        db_menu = self.model(**menu.model_dump())
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return db_menu

    async def update(self, menu: MenuUpdate, menu_id: UUID4):
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalar_one_or_none()
        # ADD IF NOT MENU THAN...
        menu_data = menu.model_dump(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return db_menu

    async def delete(self, menu_id: UUID4):
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalar_one_or_none()
        await self.session.delete(db_menu)
        await self.session.commit()

class MenuCacheRepository(BaseRedisCacheRepository):
    ...