from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from LR3.app.models import Order, OrderItem


def _to_dict(data) -> dict:
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_none=True)
    return data


class OrderRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def create(self, user_id: int, items: List[dict], total_amount: float, status: str = "pending") -> Order:
        order = Order(user_id=user_id, total_amount=total_amount, status=status)
        for item in items:
            order.items.append(
                OrderItem(
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                )
            )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        await self.session.refresh(order, attribute_names=["items"])
        return order

    async def update(self, order_id: int, **order_data) -> Optional[Order]:
        order = await self.session.get(Order, order_id)
        if not order:
            return None
        for key, value in _to_dict(order_data).items():
            if value is not None:
                setattr(order, key, value)
        await self.session.commit()
        await self.session.refresh(order)
        await self.session.refresh(order, attribute_names=["items"])
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.session.get(Order, order_id)
        if not order:
            return False
        await self.session.delete(order)
        await self.session.commit()
        return True
