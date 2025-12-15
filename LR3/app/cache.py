from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel

try:
    from redis.exceptions import RedisError  # pylint: disable=import-error
except ImportError:  # pragma: no cover

    class RedisError(Exception):
        pass


ModelT = TypeVar("ModelT", bound=BaseModel)

USER_CACHE_TTL_SECONDS = 60 * 60
PRODUCT_CACHE_TTL_SECONDS = 10 * 60


@dataclass(frozen=True)
class RedisCache:
    client: Any

    async def get_model(self, key: str, model: Type[ModelT]) -> Optional[ModelT]:
        try:
            raw = await self.client.get(key)
        except RedisError:
            return None

        if raw is None:
            return None

        try:
            return model.model_validate_json(raw)
        except (TypeError, ValueError):
            await self.delete(key)
            return None

    async def set_model(self, key: str, value: BaseModel, ttl_seconds: int) -> None:
        try:
            await self.client.set(key, value.model_dump_json(), ex=ttl_seconds)
        except RedisError:
            return

    async def delete(self, key: str) -> None:
        try:
            await self.client.delete(key)
        except RedisError:
            return
