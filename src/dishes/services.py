import pickle

from fastapi import Depends
from pydantic import UUID4

from src.dishes.repositories import DishCacheRepository, DishRepository
from src.dishes.schemas import DishCreate, DishUpdate


class DishService:
    def __init__(
        self,
        dish_repository: DishRepository = Depends(),
        dish_cache_repository: DishCacheRepository = Depends(),
    ):
        self.dish_repository: DishRepository = dish_repository
        self.dish_cache_repository: DishCacheRepository = dish_cache_repository

    async def get(self, dish_id: UUID4):
        key = str(dish_id) + self.__class__.__name__

        if dish_entity_cache := await self.dish_cache_repository.get(key):
            return dish_entity_cache

        if dish_entity_db := await self.dish_repository.get(dish_id):
            await self.dish_cache_repository.set(key, pickle.dumps(dish_entity_db))
        return dish_entity_db

    async def list(self, submenu_id: UUID4):
        dishes_list = await self.dish_repository.list(submenu_id)
        return dishes_list

    async def create(self, dish_data: DishCreate, submenu_id: UUID4):
        dish_entity = await self.dish_repository.create(dish_data, submenu_id)

        if menus_cache_keys := await self.dish_cache_repository.keys(b'*MenuService*'):
            await self.dish_cache_repository.delete(*menus_cache_keys)

        if submenus_cache_keys := await self.dish_cache_repository.keys(b'*SubmenuService*'):
            await self.dish_cache_repository.delete(*submenus_cache_keys)

        return dish_entity

    async def update(self, dish_data: DishUpdate, dish_id: UUID4):
        key = str(dish_id) + self.__class__.__name__

        dish_entity = await self.dish_repository.update(dish_data, dish_id)

        await self.dish_cache_repository.set(key, pickle.dumps(dish_entity))

        return dish_entity

    async def delete(self, dish_id: UUID4):
        key = str(dish_id) + self.__class__.__name__

        await self.dish_cache_repository.delete(key)

        if menus_cache_keys := await self.dish_cache_repository.keys(b'*MenuService*'):
            await self.dish_cache_repository.delete(*menus_cache_keys)

        if submenus_cache_keys := await self.dish_cache_repository.keys(b'*SubmenuService*'):
            await self.dish_cache_repository.delete(*submenus_cache_keys)

        return await self.dish_repository.delete(dish_id)
