from math import ceil
from typing import TypeVar

from fastapi import Query
from sqlalchemy.orm import Query as SAQuery

from app.schemas.pagination import PaginatedResponse

T = TypeVar("T")

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


def pagination_params(
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number"),
    page_size: int = Query(
        DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description="Number of items per page",
    ),
) -> dict:
    return {"page": page, "page_size": page_size}


def paginate(query: SAQuery, page: int, page_size: int) -> PaginatedResponse:
    total = query.count()
    items = (
        query.offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    pages = ceil(total / page_size) if page_size and total else 0

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )
