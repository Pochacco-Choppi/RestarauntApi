import pickle

from fastapi import Depends
from pydantic import UUID4

from src.menus.repositories import MenuCacheRepository, MenuRepository
from src.menus.schemas import MenuCreate, MenuUpdate


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository = Depends(),
        menu_cache_repository: MenuCacheRepository = Depends(),
    ):
        self.menu_repository: MenuRepository = menu_repository
        self.menu_cache_repository: MenuCacheRepository = menu_cache_repository

    async def get(self, menu_id: UUID4):
        key = str(menu_id) + self.__class__.__name__

        if menu_entity_cache := await self.menu_cache_repository.get(key):
            return menu_entity_cache

        if menu_entity_db := await self.menu_repository.get(menu_id):
            await self.menu_cache_repository.set(key, pickle.dumps(menu_entity_db))
        return menu_entity_db

    async def list(self, skip: int = 0, limit: int = 100):
        menus_list = await self.menu_repository.list()
        return menus_list

    async def create(self, menu: MenuCreate):
        menu_entity = await self.menu_repository.create(menu)
        return menu_entity

    async def update(self, menu: MenuUpdate, menu_id: UUID4):
        key = str(menu_id) + self.__class__.__name__

        menu_entity = await self.menu_repository.update(menu, menu_id)
        await self.menu_cache_repository.set(key, pickle.dumps(menu_entity))

        return menu_entity

    async def delete(self, menu_id: UUID4):
        key = str(menu_id) + self.__class__.__name__

        await self.menu_cache_repository.delete(key)

        return await self.menu_repository.delete(menu_id)