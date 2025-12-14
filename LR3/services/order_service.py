from __future__ import annotations

from typing import List, Union

from LR3.app.schemas import OrderCreate, OrderUpdate
from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    async def get_by_id(self, order_id: int):
        return await self.order_repository.get_by_id(order_id)

    async def get_all(self, limit: int = 100, offset: int = 0):
        return await self.order_repository.get_all(limit, offset)

    async def create_order(self, order_data: Union[OrderCreate, dict]):
        if isinstance(order_data, dict):
            order_data = OrderCreate(**order_data)

        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError("User not found")

        items_payload: List[dict] = []
        total_amount = 0.0
        products_for_update = []

        for item in order_data.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise ValueError("Product not found")
            if product.stock_quantity < item.quantity:
                raise ValueError("Insufficient stock")

            products_for_update.append((product, item.quantity))
            items_payload.append(
                {
                    "product_id": product.id,
                    "quantity": item.quantity,
                    "price": product.price,
                }
            )
            total_amount += product.price * item.quantity

        order = await self.order_repository.create(
            user_id=order_data.user_id,
            items=items_payload,
            total_amount=total_amount,
            status="pending",
        )

        for product, qty in products_for_update:
            await self.product_repository.update(
                product.id,
                stock_quantity=product.stock_quantity - qty,
            )

        return order

    async def update(self, order_id: int, order_data: Union[OrderUpdate, dict]):
        if isinstance(order_data, dict):
            order_data = OrderUpdate(**order_data)
        payload = order_data.model_dump(exclude_none=True)
        return await self.order_repository.update(order_id, **payload)

    async def delete(self, order_id: int):
        return await self.order_repository.delete(order_id)
