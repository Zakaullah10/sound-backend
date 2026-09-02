from pydantic import BaseModel
from typing import Optional


class GenreCreate(BaseModel):
    category_id: Optional[int] = None
    name: str
    slug: str
    is_featured: bool = False
    display_order: Optional[int] = None


class GenreUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    is_featured: Optional[bool] = None
    display_order: Optional[int] = None


class GenreResponse(BaseModel):
    id: int
    category_id: Optional[int]
    name: str
    slug: str
    is_featured: bool
    display_order: Optional[int]

    class Config:
        from_attributes = True

