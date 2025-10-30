from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey, Float, select
from sqlalchemy.orm import declarative_base, mapped_column, relationship, Mapped, selectinload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column(nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    product = relationship("Product", back_populates="orders")


connect_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/my_postgres_db"
engine = create_engine(connect_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # создаём таблицы

    with SessionLocal() as session:
        # Добавляем 1 пользователя
        user = User(
            username="user1",
            email="user1@example.com",
            description="Описание пользователя 1"
        )
        session.add(user)
        session.flush()  # чтобы присвоился id

        # Добавляем адрес для пользователя
        address = Address(
            user_id=user.id,
            street="Street 1",
            city="City 1",
            country="Country",
            is_primary=True
        )
        session.add(address)

        # Добавляем продукт
        product = Product(
            name="Product 1",
            price=100.0
        )
        session.add(product)
        session.flush()

        # Добавляем заказ
        order = Order(
            user_id=user.id,
            address_id=address.id,
            product_id=product.id,
            quantity=2
        )
        session.add(order)

        session.commit()

    # Пример запроса
    with SessionLocal() as session:
        users = session.execute(select(User).options(selectinload(User.addresses))).scalars().all()
        for u in users:
            print(u.username, u.description, [a.street for a in u.addresses])
