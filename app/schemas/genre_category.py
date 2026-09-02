from pydantic import BaseModel
from typing import Optional


class GenreCategoryCreate(BaseModel):
    name: str
    slug: str
    display_order: Optional[int] = None


class GenreCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    display_order: Optional[int] = None


class GenreCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    display_order: Optional[int]

    class Config:
        from_attributes = True

