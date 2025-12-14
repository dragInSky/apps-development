from LR3.app.schemas import ProductCreate, ProductUpdate
from LR3.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: int):
        return await self.product_repository.get_by_id(product_id)

    async def get_all(self, limit: int = 100, offset: int = 0):
        return await self.product_repository.get_all(limit, offset)

    async def create(self, product_data: ProductCreate):
        return await self.product_repository.create(**product_data.model_dump())

    async def update(self, product_id: int, product_data: ProductUpdate):
        payload = product_data.model_dump(exclude_none=True)
        return await self.product_repository.update(product_id, **payload)

    async def delete(self, product_id: int):
        return await self.product_repository.delete(product_id)

    async def adjust_stock(self, product_id: int, delta: int):
        return await self.product_repository.adjust_stock(product_id, delta)
