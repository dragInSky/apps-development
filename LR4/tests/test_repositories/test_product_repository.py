import pytest

from LR3.repositories.product_repository import ProductRepository


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            name="Wireless Mouse",
            price=27.5,
            stock_quantity=15,
            description="Office mouse",
        )

        assert product.id is not None
        assert product.stock_quantity == 15
        assert product.price == 27.5

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            name="Phone Case",
            price=10.0,
            stock_quantity=5,
        )

        updated = await product_repository.update(
            product.id,
            name="Case Updated",
            stock_quantity=7,
        )

        assert updated.name == "Case Updated"
        assert updated.stock_quantity == 7

    @pytest.mark.asyncio
    async def test_get_all_products(self, product_repository: ProductRepository):
        await product_repository.create(name="A", price=5.0, stock_quantity=1)
        await product_repository.create(name="B", price=6.0, stock_quantity=2)

        products = await product_repository.get_all()

        assert len(products) >= 2

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            name="Old Charger",
            price=12.0,
            stock_quantity=1,
        )

        deleted = await product_repository.delete(product.id)
        missing = await product_repository.get_by_id(product.id)

        assert deleted is True
        assert missing is None
