import pytest

from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_create_order_with_multiple_items(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        user = await user_repository.create(
            email="ordersample@gmail.com",
            username="order_user",
            first_name="Artem",
            last_name="Rudenko",
        )
        product1 = await product_repository.create(name="USB Cable", price=5.5, stock_quantity=5)
        product2 = await product_repository.create(name="Power Bank", price=30.0, stock_quantity=10)

        total = product1.price * 2 + product2.price * 3
        order = await order_repository.create(
            user_id=user.id,
            items=[
                {"product_id": product1.id, "quantity": 2, "price": product1.price},
                {"product_id": product2.id, "quantity": 3, "price": product2.price},
            ],
            total_amount=total,
        )

        assert order.id is not None
        assert order.total_amount == total
        assert len(order.items) == 2
        assert {item.product_id for item in order.items} == {product1.id, product2.id}

    @pytest.mark.asyncio
    async def test_get_and_update_order(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        user = await user_repository.create(
            email="statuscheck@gmail.com",
            username="status_user",
            first_name="Mikhail",
            last_name="Status",
        )
        product = await product_repository.create(name="Cable", price=10.0, stock_quantity=5)

        order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1, "price": product.price}],
            total_amount=product.price,
        )

        fetched = await order_repository.get_by_id(order.id)
        assert fetched is not None
        assert len(fetched.items) == 1

        updated = await order_repository.update(order.id, status="shipped")
        assert updated.status == "shipped"

    @pytest.mark.asyncio
    async def test_delete_order(
        self,
        order_repository: OrderRepository,
        user_repository: UserRepository,
        product_repository: ProductRepository,
    ):
        user = await user_repository.create(
            email="removeorder@gmail.com",
            username="delete_user",
            first_name="Pavel",
            last_name="Smirnov",
        )
        product = await product_repository.create(name="Cable", price=10.0, stock_quantity=5)

        order = await order_repository.create(
            user_id=user.id,
            items=[{"product_id": product.id, "quantity": 1, "price": product.price}],
            total_amount=product.price,
        )

        deleted = await order_repository.delete(order.id)
        missing = await order_repository.get_by_id(order.id)

        assert deleted is True
        assert missing is None
