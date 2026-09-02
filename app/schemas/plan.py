from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PlanCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration_days: int
    stripe_price_id: str
    stripe_product_id: Optional[str] = None
    is_active: bool = True


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_days: Optional[int] = None
    stripe_price_id: Optional[str] = None
    stripe_product_id: Optional[str] = None
    is_active: Optional[bool] = None


class PlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    duration_days: int
    stripe_price_id: str
    stripe_product_id: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True