import pickle
from typing import Any

from fastapi import Depends
from pydantic import UUID4

from src.menus.repositories import MenuCacheRepository, MenuRepository
from src.menus.schemas import MenuCreate, MenuUpdate


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository = Depends(),
        menu_cache_repository: MenuCacheRepository = Depends(),
    ) -> None:
        self.menu_repository: MenuRepository = menu_repository
        self.menu_cache_repository: MenuCacheRepository = menu_cache_repository

    def generate_cache_key(self, menu_id: UUID4) -> str:
        key = f'{str(menu_id)}'
        return key

    async def get(self, menu_id: UUID4) -> Any:
        key = self.generate_cache_key(menu_id)

        if menu_entity_cache := await self.menu_cache_repository.get(key):
            return menu_entity_cache

        if menu_entity_db := await self.menu_repository.get(menu_id):
            await self.menu_cache_repository.set(key, pickle.dumps(menu_entity_db))
        return menu_entity_db

    async def list(self, skip: int = 0, limit: int = 100) -> Any:
        menus_list = await self.menu_repository.list()
        return menus_list

    async def list_related(self, skip: int = 0, limit: int = 100) -> Any:
        menus_list = await self.menu_repository.list_related()
        return menus_list

    async def create(self, menu: MenuCreate) -> Any:
        menu_entity = await self.menu_repository.create(menu)
        return menu_entity

    async def update(self, menu: MenuUpdate, menu_id: UUID4) -> Any:
        key = self.generate_cache_key(menu_id)

        menu_entity = await self.menu_repository.update(menu, menu_id)
        await self.menu_cache_repository.set(key, pickle.dumps(menu_entity))

        return menu_entity

    async def clear_cache(self, menu_id: UUID4):
        key = self.generate_cache_key(menu_id)
        await self.menu_cache_repository.delete(key)

        if related_cache_keys := await self.menu_cache_repository.keys(f'*{menu_id}*'.encode()):
            await self.menu_cache_repository.delete(*related_cache_keys)

    async def delete(self, menu_id: UUID4) -> Any:

        return await self.menu_repository.delete(menu_id)

    async def bulk_create(self, menus):
        return await self.menu_repository.bulk_create(menus)
