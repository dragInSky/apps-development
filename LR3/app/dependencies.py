import os
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from LR3.app.cache import RedisCache
from LR3.app.models import Base
from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.report_repository import ReportRepository
from LR3.repositories.user_repository import UserRepository
from LR3.services.order_service import OrderService
from LR3.services.product_service import ProductService
from LR3.services.report_service import ReportService
from LR3.services.user_service import UserService

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/my_postgres_db"
)

try:
    from redis.asyncio import Redis  # pylint: disable=import-error
except ImportError:  # pragma: no cover
    Redis = Any  # type: ignore[misc,assignment]

_redis_client: Optional[Any] = None


def make_engine(url: Optional[str] = None):
    return create_async_engine(url or DATABASE_URL, echo=False)


engine = make_engine()
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

ORDER_REPORT_VIEW_NAME = "order_report"
ORDER_REPORT_VIEW_SQL = f"""
CREATE VIEW {ORDER_REPORT_VIEW_NAME} AS
SELECT
    DATE(o.created_at) AS report_at,
    o.id AS order_id,
    COALESCE(SUM(oi.quantity), 0) AS count_product
FROM orders AS o
LEFT JOIN order_items AS oi ON oi.order_id = o.id
GROUP BY DATE(o.created_at), o.id;
""".strip()


def configure_engine(new_url: Optional[str] = None) -> None:
    """Recreate engine and session factory (useful for tests)."""
    global engine, async_session_factory
    engine = make_engine(new_url)
    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(f"DROP VIEW IF EXISTS {ORDER_REPORT_VIEW_NAME};"))
        await conn.execute(text(ORDER_REPORT_VIEW_SQL))


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


async def provide_order_repository(db_session: AsyncSession) -> OrderRepository:
    return OrderRepository(db_session)


async def provide_report_repository(db_session: AsyncSession) -> ReportRepository:
    return ReportRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


async def provide_product_service(
    product_repository: ProductRepository,
) -> ProductService:
    return ProductService(product_repository)


async def provide_order_service(
    order_repository: OrderRepository,
    product_repository: ProductRepository,
    user_repository: UserRepository,
) -> OrderService:
    return OrderService(order_repository, product_repository, user_repository)


async def provide_report_service(
    report_repository: ReportRepository,
) -> ReportService:
    return ReportService(report_repository)


def get_redis_client() -> Any:
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        _redis_client = Redis.from_url(redis_url, decode_responses=True)
        return _redis_client

    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", "6379"))
    db = int(os.getenv("REDIS_DB", "0"))
    _redis_client = Redis(host=host, port=port, db=db, decode_responses=True)
    return _redis_client


async def provide_redis() -> Any:
    return get_redis_client()


async def provide_cache(redis_client: Any) -> RedisCache:
    return RedisCache(redis_client)
