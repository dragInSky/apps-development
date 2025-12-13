import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from LR3.repositories.user_repository import UserRepository
from LR3.services.user_service import UserService
from LR3.app.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/my_postgres_db")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)
