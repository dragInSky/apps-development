from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = {"extra": "forbid", "from_attributes": True}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    model_config = {"extra": "forbid", "from_attributes": True}


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int = Field(ge=0)
    description: Optional[str] = None

    model_config = {"extra": "forbid", "from_attributes": True}


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None

    model_config = {"extra": "forbid", "from_attributes": True}


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

    model_config = {"extra": "forbid"}


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemRequest]

    model_config = {"extra": "forbid"}


class OrderUpdate(BaseModel):
    status: Optional[str] = None

    model_config = {"extra": "forbid"}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    items: List[OrderItemResponse]

    model_config = {"from_attributes": True}


class ReportRequest(BaseModel):
    report_at: date

    model_config = {"extra": "forbid"}


class ReportRow(BaseModel):
    report_at: date
    order_id: int
    count_product: int

    model_config = {"extra": "forbid"}
