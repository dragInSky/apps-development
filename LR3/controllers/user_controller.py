from typing import List
from litestar import Controller, get, post, put, delete
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from LR3.app.schemas import UserResponse, UserCreate, UserUpdate
from LR3.services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(self, user_service: UserService, user_id: int = Parameter(gt=0)) -> UserResponse:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(self, user_service: UserService) -> List[UserResponse]:
        users = await user_service.get_by_filter(count=100, page=1)
        return [UserResponse.model_validate(u) for u in users]

    @post()
    async def create_user(self, user_service: UserService, data: UserCreate) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @put("/{user_id:int}")
    async def update_user(self, user_service: UserService, data: UserUpdate, user_id: int = Parameter(gt=0)) -> UserResponse:
        user = await user_service.update(user_id, data)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(self, user_service: UserService, user_id: int = Parameter(gt=0)) -> None:
        deleted = await user_service.delete(user_id)
        if deleted is None:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
