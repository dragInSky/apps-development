from datetime import datetime
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import sys
import os
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)  # добавляем корень в sys.path

from main import Base, User, Address, Product, Order, engine, SessionLocal

# Создаём все таблицы (если ещё не созданы)
Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    users = []
    addresses = []
    products = []
    orders = []

    # --- 5 пользователей и адресов ---
    for i in range(1, 6):
        user = User(
            username=f"user{i}",
            email=f"user{i}@example.com",
            description=f"Описание пользователя {i}"
        )
        session.add(user)
        session.flush()  # чтобы присвоился user.id

        address = Address(
            user_id=user.id,
            street=f"Street {i}",
            city=f"City {i}",
            state=f"State {i}",
            zip_code=f"0000{i}",
            country="Country",
            is_primary=True
        )
        session.add(address)

        users.append(user)
        addresses.append(address)

    # --- 5 продуктов ---
    for i in range(1, 6):
        product = Product(
            name=f"Product {i}",
            price=10.0 * i
        )
        session.add(product)
        session.flush()
        products.append(product)

    # --- 5 заказов (каждому пользователю один заказ) ---
    for i in range(5):
        order = Order(
            user_id=users[i].id,
            address_id=addresses[i].id,
            product_id=products[i].id,
            quantity=i+1
        )
        session.add(order)
        orders.append(order)

    session.commit()

# --- Вывод данных ---
with SessionLocal() as session:
    print("Пользователи и их адреса:")
    for u in session.execute(select(User).options(selectinload(User.addresses))).scalars().all():
        print(u.username, u.description, [(a.street, a.city, a.state) for a in u.addresses])

    print("\nПродукты:")
    for p in session.execute(select(Product)).scalars().all():
        print(p.name, p.price)

    print("\nЗаказы:")
    for o in session.execute(select(Order).options(
        selectinload(Order.user),
        selectinload(Order.address),
        selectinload(Order.product)
    )).scalars().all():
        print(f"Заказ {o.id}: пользователь {o.user.username}, адрес {o.address.street}, продукт {o.product.name}, количество {o.quantity}")