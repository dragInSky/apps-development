from typing import List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED

from LR3.app.schemas import ProductCreate, ProductResponse, ProductUpdate
from LR3.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"

    @get()
    async def list_products(self, product_service: ProductService) -> List[ProductResponse]:
        products = await product_service.get_all()
        return [ProductResponse.model_validate(p) for p in products]

    @get("/{product_id:int}")
    async def get_product(
        self,
        product_service: ProductService,
        product_id: int = Parameter(gt=0),
    ) -> ProductResponse:
        product = await product_service.get_by_id(product_id)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product)

    @post(status_code=HTTP_201_CREATED)
    async def create_product(self, product_service: ProductService, data: ProductCreate) -> ProductResponse:
        product = await product_service.create(data)
        return ProductResponse.model_validate(product)

    @put("/{product_id:int}")
    async def update_product(
        self,
        product_service: ProductService,
        data: ProductUpdate,
        product_id: int = Parameter(gt=0),
    ) -> ProductResponse:
        product = await product_service.update(product_id, data)
        if not product:
            raise NotFoundException(f"Product with ID {product_id} not found")
        return ProductResponse.model_validate(product)

    @delete("/{product_id:int}")
    async def delete_product(
        self,
        product_service: ProductService,
        product_id: int = Parameter(gt=0),
    ) -> None:
        deleted = await product_service.delete(product_id)
        if not deleted:
            raise NotFoundException(f"Product with ID {product_id} not found")
