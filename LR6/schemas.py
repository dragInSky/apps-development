from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from LR3.app.schemas import OrderCreate, ProductCreate, ProductUpdate


class ProductCreateMessage(BaseModel):
    action: Literal["create"]
    product: ProductCreate

    model_config = {"extra": "forbid"}


class ProductUpdateMessage(BaseModel):
    action: Literal["update"]
    product_id: int = Field(gt=0)
    product: ProductUpdate

    model_config = {"extra": "forbid"}


class ProductOutOfStockMessage(BaseModel):
    action: Literal["out_of_stock"]
    product_id: int = Field(gt=0)

    model_config = {"extra": "forbid"}


ProductMessage = Annotated[
    Union[ProductCreateMessage, ProductUpdateMessage, ProductOutOfStockMessage],
    Field(discriminator="action"),
]


class OrderCreateMessage(BaseModel):
    action: Literal["create"]
    order: OrderCreate

    model_config = {"extra": "forbid"}


class OrderUpdateStatusMessage(BaseModel):
    action: Literal["update_status"]
    order_id: int = Field(gt=0)
    status: str = Field(min_length=1, max_length=50)

    model_config = {"extra": "forbid"}


OrderMessage = Annotated[
    Union[OrderCreateMessage, OrderUpdateStatusMessage],
    Field(discriminator="action"),
]
