import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from LR3.app.models import Base
from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository
from LR3.services.order_service import OrderService
from LR3.services.product_service import ProductService
from LR3.services.user_service import UserService

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/my_postgres_db")


def make_engine(url: Optional[str] = None):
    return create_async_engine(url or DATABASE_URL, echo=False)


engine = make_engine()
async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def configure_engine(new_url: Optional[str] = None) -> None:
    """Recreate engine and session factory (useful for tests)."""
    global engine, async_session_factory
    engine = make_engine(new_url)
    async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


async def provide_order_repository(db_session: AsyncSession) -> OrderRepository:
    return OrderRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


async def provide_product_service(product_repository: ProductRepository) -> ProductService:
    return ProductService(product_repository)


async def provide_order_service(
    order_repository: OrderRepository,
    product_repository: ProductRepository,
    user_repository: UserRepository,
) -> OrderService:
    return OrderService(order_repository, product_repository, user_repository)
