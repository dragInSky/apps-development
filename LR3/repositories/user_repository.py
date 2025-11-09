from typing import List
from sqlalchemy import select
from LR3.app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, user_id: int):
        return await self.session.get(User, user_id)

    async def get_by_filter(self, count: int, page: int, **kwargs) -> List[User]:
        stmt = select(User).limit(count).offset((page - 1) * count)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, user_data):
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data):
        user = await self.session.get(User, user_id)
        if not user:
            return None
        for key, value in user_data.model_dump(exclude_none=True).items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int):
        user = await self.session.get(User, user_id)
        if not user:
            return None
        await self.session.delete(user)
        await self.session.commit()
