from typing import Any

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import and_, func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRedisCacheRepository
from src.dependencies import get_session
from src.dishes.models import Dish
from src.menus.models import Menu
from src.menus.schemas import MenuCreate, MenuUpdate
from src.submenus.models import Submenu


class MenuRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session: AsyncSession = session
        self.model = Menu

    async def get_by_id(self, menu_id: UUID4) -> Menu | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(stmt)
        db_menu = result.scalar_one_or_none()
        return db_menu

    async def get(self, menu_id: UUID4) -> Any:
        stmt = (
            select(
                self.model.id,
                self.model.title,
                self.model.description,
                select(func.count(Submenu.id))
                .where(Submenu.menu_id == menu_id)
                .label('submenus_count'),
                select(func.count(Dish.id))
                .join(Submenu)
                .where(and_(Submenu.menu_id == menu_id, Submenu.id == Dish.submenu_id))
                .label('dishes_count'),
            )
            .where(self.model.id == menu_id)
            .select_from(self.model)
            .group_by(self.model.id)
        )
        result = await self.session.execute(stmt)

        return result.mappings().one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Menu]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def list_related(self, skip: int = 0, limit: int = 100) -> Any:
        stmt = select(self.model).options(
            joinedload(self.model.submenus)
            .options(joinedload(Submenu.dishes))
        ).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def create(self, menu: MenuCreate) -> Menu:
        db_menu = self.model(**menu.model_dump())
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return db_menu

    async def update(self, menu: MenuUpdate, menu_id: UUID4) -> Menu | None:
        db_menu = await self.get_by_id(menu_id)
        # ADD IF NOT MENU THAN...
        menu_data = menu.model_dump(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return db_menu

    async def delete(self, menu_id: UUID4) -> None:
        db_menu = await self.get_by_id(menu_id)
        await self.session.delete(db_menu)
        await self.session.commit()


class MenuCacheRepository(BaseRedisCacheRepository):
    ...
