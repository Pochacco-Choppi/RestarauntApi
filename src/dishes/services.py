import pickle
from typing import Any

from fastapi import Depends
from pydantic import UUID4

from src.dishes.repositories import DishCacheRepository, DishRepository
from src.dishes.schemas import DishCreate, DishUpdate


class DishService:
    def __init__(
        self,
        dish_repository: DishRepository = Depends(),
        dish_cache_repository: DishCacheRepository = Depends(),
    ) -> None:
        self.dish_repository: DishRepository = dish_repository
        self.dish_cache_repository: DishCacheRepository = dish_cache_repository

    def generate_cache_key(self, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4) -> str:
        key = f'{str(menu_id)}:{str(submenu_id)}:{str(dish_id)}'
        return key

    async def get(self, dish_id: UUID4, menu_id: UUID4, submenu_id: UUID4,) -> Any:
        key = self.generate_cache_key(menu_id, submenu_id, dish_id)

        if dish_entity_cache := await self.dish_cache_repository.get(key):
            return dish_entity_cache

        if dish_entity_db := await self.dish_repository.get(dish_id):
            await self.dish_cache_repository.set(key, pickle.dumps(dish_entity_db))
        return dish_entity_db

    async def list(self, submenu_id: UUID4) -> Any:
        dishes_list = await self.dish_repository.list(submenu_id)
        return dishes_list

    async def create(self, dish_data: DishCreate, submenu_id: UUID4, menu_id: UUID4) -> Any:
        dish_entity = await self.dish_repository.create(dish_data, submenu_id)

        if menus_cache_keys := await self.dish_cache_repository.keys(f'*{menu_id}*'.encode()):
            await self.dish_cache_repository.delete(*menus_cache_keys)

        if submenus_cache_keys := await self.dish_cache_repository.keys(f'*{submenu_id}*'.encode()):
            await self.dish_cache_repository.delete(*submenus_cache_keys)

        return dish_entity

    async def update(self, dish_data: DishUpdate, dish_id: UUID4, menu_id: UUID4, submenu_id: UUID4) -> Any:
        key = self.generate_cache_key(menu_id, submenu_id, dish_id)

        dish_entity = await self.dish_repository.update(dish_data, dish_id)

        await self.dish_cache_repository.set(key, pickle.dumps(dish_entity))

        return dish_entity

    async def clear_cache(self, dish_id: UUID4, menu_id: UUID4, submenu_id: UUID4):
        key = self.generate_cache_key(menu_id, submenu_id, dish_id)

        await self.dish_cache_repository.delete(key)

        if menus_cache_keys := await self.dish_cache_repository.keys(f'*{menu_id}*'.encode()):
            await self.dish_cache_repository.delete(*menus_cache_keys)

        if submenus_cache_keys := await self.dish_cache_repository.keys(f'*{submenu_id}*'.encode()):
            await self.dish_cache_repository.delete(*submenus_cache_keys)

    async def delete(self, dish_id: UUID4, menu_id: UUID4, submenu_id: UUID4) -> Any:

        return await self.dish_repository.delete(dish_id)
