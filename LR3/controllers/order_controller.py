from typing import List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from litestar.status_codes import HTTP_201_CREATED

from LR3.app.schemas import OrderCreate, OrderResponse, OrderUpdate
from LR3.services.order_service import OrderService


class OrderController(Controller):
    path = "/orders"

    @get()
    async def list_orders(self, order_service: OrderService) -> List[OrderResponse]:
        orders = await order_service.get_all()
        return [OrderResponse.model_validate(o) for o in orders]

    @get("/{order_id:int}")
    async def get_order(
        self,
        order_service: OrderService,
        order_id: int = Parameter(gt=0),
    ) -> OrderResponse:
        order = await order_service.get_by_id(order_id)
        if not order:
            raise NotFoundException(f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order)

    @post(status_code=HTTP_201_CREATED)
    async def create_order(
        self, order_service: OrderService, data: OrderCreate
    ) -> OrderResponse:
        order = await order_service.create_order(data)
        return OrderResponse.model_validate(order)

    @put("/{order_id:int}")
    async def update_order(
        self,
        order_service: OrderService,
        data: OrderUpdate,
        order_id: int = Parameter(gt=0),
    ) -> OrderResponse:
        order = await order_service.update(order_id, data)
        if not order:
            raise NotFoundException(f"Order with ID {order_id} not found")
        return OrderResponse.model_validate(order)

    @delete("/{order_id:int}")
    async def delete_order(
        self, order_service: OrderService, order_id: int = Parameter(gt=0)
    ) -> None:
        deleted = await order_service.delete(order_id)
        if not deleted:
            raise NotFoundException(f"Order with ID {order_id} not found")
