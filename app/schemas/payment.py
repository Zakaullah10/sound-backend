from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CheckoutSessionCreate(BaseModel):
    plan_id: int


class CheckoutSessionResponse(BaseModel):
    checkout_url: str


class PaymentResponse(BaseModel):
    id: int
    amount: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True