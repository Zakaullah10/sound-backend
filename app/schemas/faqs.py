from pydantic import BaseModel
from typing import Optional

class FAQBase(BaseModel):
    question: str
    answer: str
    display_order: Optional[int] = None
    is_active: Optional[bool] = True

class FAQCreate(FAQBase):
    pass

class FAQUpdate(FAQBase):
    pass

class FAQResponse(FAQBase):
    id: int
    class Config:
        from_attributes = True