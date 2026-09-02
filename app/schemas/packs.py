from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal


class PackCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None
    price: Decimal = 0
    is_free: bool = False
    status: str = "draft"
    genre_id: Optional[int] = None
    label_ids: List[int] = []


class PackResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    cover_image: Optional[str]
    price: Decimal
    is_free: bool
    status: str
    genre_id: Optional[int]

    class Config:
        from_attributes = True


class PackLabelResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class PackDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Decimal
    is_free: bool
    status: str
    genre_id: Optional[int]
    labels: List[PackLabelResponse] = []

    class Config:
        from_attributes = True