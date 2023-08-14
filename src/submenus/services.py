import pickle
from typing import Any

from fastapi import Depends
from pydantic import UUID4

from src.submenus.repositories import SubmenuCacheRepository, SubmenuRepository
from src.submenus.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuService:
    def __init__(
        self,
        sumbmenu_repository: SubmenuRepository = Depends(),
        submenu_cache_repository: SubmenuCacheRepository = Depends(),
    ) -> None:
        self.submenu_repository: SubmenuRepository = sumbmenu_repository
        self.submenu_cache_repository: SubmenuCacheRepository = submenu_cache_repository

    def generate_cache_key(self, menu_id: UUID4, submenu_id: UUID4) -> str:
        key = f'{str(menu_id)}:{str(submenu_id)}'
        return key

    async def get(self, submenu_id: UUID4, menu_id: UUID4) -> Any:
        key = self.generate_cache_key(menu_id, submenu_id)

        if submenu_entity_cache := await self.submenu_cache_repository.get(key):
            return submenu_entity_cache

        if submenu_entity_db := await self.submenu_repository.get(submenu_id):
            await self.submenu_cache_repository.set(key, pickle.dumps(submenu_entity_db))
        return submenu_entity_db

    async def list(self, menu_id: UUID4, skip: int = 0, limit: int = 100) -> Any:
        submenus_list = await self.submenu_repository.list(menu_id)
        return submenus_list

    async def create(self, submenu: SubmenuCreate, menu_id: UUID4) -> Any:
        submenu_entity = await self.submenu_repository.create(submenu, menu_id)

        if menus_cache_keys := await self.submenu_cache_repository.keys(f'*{menu_id}*'.encode()):
            await self.submenu_cache_repository.delete(*menus_cache_keys)

        return submenu_entity

    async def update(self, submenu: SubmenuUpdate, submenu_id: UUID4, menu_id: UUID4) -> Any:
        key = self.generate_cache_key(menu_id, submenu_id)

        submenu_entity = await self.submenu_repository.update(submenu, submenu_id)
        await self.submenu_cache_repository.set(key, pickle.dumps(submenu_entity))

        return submenu_entity

    async def clear_cache(self, submenu_id: UUID4, menu_id: UUID4):
        key = self.generate_cache_key(menu_id, submenu_id)

        await self.submenu_cache_repository.delete(key)

        if menus_cache_keys := await self.submenu_cache_repository.keys(f'*{menu_id}*'.encode()):
            await self.submenu_cache_repository.delete(*menus_cache_keys)

    async def delete(self, submenu_id: UUID4, menu_id: UUID4) -> Any:
        return await self.submenu_repository.delete(submenu_id)
