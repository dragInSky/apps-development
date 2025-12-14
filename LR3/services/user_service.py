from LR3.app.schemas import UserCreate, UserUpdate
from LR3.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int):
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str):
        return await self.user_repository.get_by_email(email)

    async def get_all(self, limit: int = 100, offset: int = 0):
        return await self.user_repository.get_all(limit, offset)

    async def create(self, user_data: UserCreate):
        return await self.user_repository.create(**user_data.model_dump())

    async def update(self, user_id: int, user_data: UserUpdate):
        payload = user_data.model_dump(exclude_none=True)
        return await self.user_repository.update(user_id, **payload)

    async def delete(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)
