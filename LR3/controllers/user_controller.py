from typing import List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import HTTPException, NotFoundException
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED, HTTP_409_CONFLICT

from LR3.app.cache import USER_CACHE_TTL_SECONDS, RedisCache
from LR3.app.schemas import UserCreate, UserResponse, UserUpdate
from LR3.services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        cache: RedisCache,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        cache_key = f"user:{user_id}"
        cached = await cache.get_model(cache_key, UserResponse)
        if cached is not None:
            return cached

        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        response = UserResponse.model_validate(user)
        await cache.set_model(cache_key, response, USER_CACHE_TTL_SECONDS)
        return response

    @get()
    async def get_all_users(self, user_service: UserService) -> List[UserResponse]:
        users = await user_service.get_all()
        return [UserResponse.model_validate(u) for u in users]

    @post(status_code=HTTP_201_CREATED)
    async def create_user(
        self, user_service: UserService, data: UserCreate
    ) -> UserResponse:
        try:
            user = await user_service.create(data)
        except ValueError as exc:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(exc)) from exc
        return UserResponse.model_validate(user)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        cache: RedisCache,
        data: UserUpdate,
        user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        try:
            user = await user_service.update(user_id, data)
        except ValueError as exc:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(exc)) from exc
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await cache.delete(f"user:{user_id}")
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        cache: RedisCache,
        user_id: int = Parameter(gt=0),
    ) -> None:
        deleted = await user_service.delete(user_id)
        if not deleted:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        await cache.delete(f"user:{user_id}")
