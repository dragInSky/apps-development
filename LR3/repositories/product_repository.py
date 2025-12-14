from typing import List, Optional

from sqlalchemy import select

from LR3.app.models import Product


def _to_dict(data) -> dict:
    if hasattr(data, "model_dump"):
        return data.model_dump(exclude_none=True)
    return data


class ProductRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self.session.get(Product, product_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Product]:
        stmt = select(Product).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **product_data) -> Product:
        payload = _to_dict(product_data)
        product = Product(**payload)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id: int, **product_data) -> Optional[Product]:
        product = await self.session.get(Product, product_id)
        if not product:
            return None
        for key, value in _to_dict(product_data).items():
            if value is not None:
                setattr(product, key, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def adjust_stock(self, product_id: int, delta: int) -> Optional[Product]:
        product = await self.session.get(Product, product_id)
        if not product:
            return None
        new_stock = product.stock_quantity + delta
        if new_stock < 0:
            return None
        product.stock_quantity = new_stock
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.session.get(Product, product_id)
        if not product:
            return False
        await self.session.delete(product)
        await self.session.commit()
        return True
