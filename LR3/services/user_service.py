from LR3.app.schemas import UserCreate, UserUpdate
from LR3.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int):
        return await self.user_repository.get_by_id(user_id)

    async def get_by_email(self, email: str):
        return await self.user_repository.get_by_email(email)

    async def get_by_username(self, username: str):
        return await self.user_repository.get_by_username(username)

    async def get_all(self, limit: int = 100, offset: int = 0):
        return await self.user_repository.get_all(limit, offset)

    async def create(self, user_data: UserCreate):
        if await self.user_repository.get_by_email(user_data.email):
            raise ValueError(f"Email already exists: {user_data.email}")
        if await self.user_repository.get_by_username(user_data.username):
            raise ValueError(f"Username already exists: {user_data.username}")
        return await self.user_repository.create(**user_data.model_dump())

    async def update(self, user_id: int, user_data: UserUpdate):
        payload = user_data.model_dump(exclude_none=True)
        if "email" in payload:
            existing = await self.user_repository.get_by_email(payload["email"])
            if existing and existing.id != user_id:
                raise ValueError(f"Email already exists: {payload['email']}")

        if "username" in payload:
            existing = await self.user_repository.get_by_username(payload["username"])
            if existing and existing.id != user_id:
                raise ValueError(f"Username already exists: {payload['username']}")
        return await self.user_repository.update(user_id, **payload)

    async def delete(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)
