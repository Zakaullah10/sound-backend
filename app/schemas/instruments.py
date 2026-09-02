from pydantic import BaseModel
from typing import Optional, List

# ---- Category ----
class InstrumentCategoryBase(BaseModel):
    name: str
    slug: str
    display_order: Optional[int] = None

class InstrumentCategoryCreate(InstrumentCategoryBase):
    pass

class InstrumentCategoryResponse(InstrumentCategoryBase):
    id: int
    class Config:
        from_attributes = True

# ---- Instrument Tag ----
class InstrumentTagBase(BaseModel):
    name: str
    slug: Optional[str] = None
    is_featured: Optional[bool] = False
    display_order: Optional[int] = None
    category_id: Optional[int] = None

class InstrumentTagCreate(InstrumentTagBase):
    pass

class InstrumentTagUpdate(InstrumentTagBase):
    pass

class InstrumentTagResponse(InstrumentTagBase):
    id: int
    class Config:
        from_attributes = True