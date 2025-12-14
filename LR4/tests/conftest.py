import pytest
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from LR3.app import dependencies as deps
from LR3.app.main import create_app
from LR3.app.models import Base
from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository


@pytest.fixture(scope="session")
def db_url(tmp_path_factory, worker_id: str):
    base_dir = tmp_path_factory.mktemp(f"data-{worker_id}")
    db_file = base_dir / "test.db"
    return f"sqlite+aiosqlite:///{db_file}"


@pytest.fixture(scope="session")
def engine(db_url):
    deps.configure_engine(db_url)
    return deps.engine


@pytest.fixture(scope="function", autouse=True)
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, tables) -> AsyncSession:
    test_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with test_session_factory() as db_session:
        yield db_session


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


@pytest.fixture
def product_repository(session):
    return ProductRepository(session)


@pytest.fixture
def order_repository(session):
    return OrderRepository(session)


@pytest.fixture
def client(engine, tables):
    app = create_app()
    with TestClient(app=app) as client:
        yield client
