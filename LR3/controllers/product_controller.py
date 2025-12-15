from typing import List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED

from LR3.app.cache import PRODUCT_CACHE_TTL_SECONDS, RedisCache
from LR3.app.schemas import ProductCreate, ProductResponse, ProductUpdate
from LR3.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"

    @get()
    async def list_products(
        self, product_service: ProductService
    ) -> List[ProductResponse]:
        products = await product_service.get_all()
        return [ProductResponse.model_validate(p) for p in products]

    @get("/{product_id:int}")
    async def get_product(
        self,
        product_service: ProductService,
        cache: RedisCache,
        product_id: int = Parameter(gt=0),
    ) -> ProductResponse:
        cache_key = f"product:{product_id}"
        cached = await cache.get_model(cache_key, ProductResponse)
        if cached is not None:
            return cached

        product = await product_service.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        response = ProductResponse.model_validate(product)
        await cache.set_model(cache_key, response, PRODUCT_CACHE_TTL_SECONDS)
        return response

    @post(status_code=HTTP_201_CREATED)
    async def create_product(
        self, product_service: ProductService, data: ProductCreate
    ) -> ProductResponse:
        product = await product_service.create(data)
        return ProductResponse.model_validate(product)

    @put("/{product_id:int}")
    async def update_product(
        self,
        product_service: ProductService,
        cache: RedisCache,
        data: ProductUpdate,
        product_id: int = Parameter(gt=0),
    ) -> ProductResponse:
        product = await product_service.update(product_id, data)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        response = ProductResponse.model_validate(product)
        await cache.set_model(
            f"product:{product_id}", response, PRODUCT_CACHE_TTL_SECONDS
        )
        return response

    @delete("/{product_id:int}")
    async def delete_product(
        self,
        product_service: ProductService,
        cache: RedisCache,
        product_id: int = Parameter(gt=0),
    ) -> None:
        deleted = await product_service.delete(product_id)
        if not deleted:
            raise NotFoundException(f"Product with ID {product_id} not found")
        await cache.delete(f"product:{product_id}")
