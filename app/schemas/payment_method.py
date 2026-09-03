from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentMethodCreate(BaseModel):
    stripe_payment_method_id: str


class PaymentMethodResponse(BaseModel):

    id: int
    user_id: int

    stripe_payment_method_id: str

    type: str

    card_brand: Optional[str] = None
    card_last4: Optional[str] = None

    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None

    is_default: bool

    created_at: datetime

    class Config:
        from_attributes = True