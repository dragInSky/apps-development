from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

    model_config = {
        "extra": "forbid",
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "extra": "forbid",
        "from_attributes": True
    }


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
