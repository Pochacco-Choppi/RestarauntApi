import pickle
from abc import ABC, abstractmethod
from typing import Any

from src.database import redis


class AbstractRedisCacheRepository(ABC):
    def __init__(self):
        self.redis = redis

    @abstractmethod
    async def get(self, key: str) -> Any:
        ...

    @abstractmethod
    async def set(self, key: str, data) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...

    @abstractmethod
    async def keys(self, pattern: str) -> None:
        ...


class BaseRedisCacheRepository(AbstractRedisCacheRepository):
    async def get(self, key: str) -> Any:
        data = await self.redis.get(key)
        if data:
            return pickle.loads(data)

        return None

    async def set(self, key, data, ex=604800) -> None:
        await self.redis.set(key, data, ex=ex)

    async def delete(self, *keys) -> None:
        return await self.redis.delete(*keys)

    async def keys(self, pattern: str | bytes):
        return await self.redis.keys(pattern)
