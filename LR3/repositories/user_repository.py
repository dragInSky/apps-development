from typing import List, Optional

from sqlalchemy import select

from LR3.app.models import User


def _to_dict(data) -> dict:
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_none=True)
    return data


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        stmt = select(User).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **user_data) -> User:
        payload = _to_dict(user_data)
        user = User(**payload)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, **user_data) -> Optional[User]:
        user = await self.session.get(User, user_id)
        if not user:
            return None
        for key, value in _to_dict(user_data).items():
            if value is not None:
                setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True
