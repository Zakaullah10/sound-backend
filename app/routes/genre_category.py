
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.genre_categories import GENRE_CATEGORIES

from app.schemas.genre_category import (
    GenreCategoryCreate,
    GenreCategoryUpdate,
    GenreCategoryResponse,
)


router = APIRouter(
    prefix="/genre-categories",
    tags=["Genre Categories"]
)


# ==========================================
# CREATE CATEGORY
# ==========================================

@router.post(
    "/",
    response_model=GenreCategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    data: GenreCategoryCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate slug
    existing_category = db.query(GENRE_CATEGORIES).filter(
        GENRE_CATEGORIES.slug == data.slug
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category slug already exists"
        )

    category = GENRE_CATEGORIES(
        name=data.name,
        slug=data.slug,
        display_order=data.display_order
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


# ==========================================
# GET ALL CATEGORIES
# ==========================================

@router.get(
    "/",
    response_model=list[GenreCategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):

    categories = db.query(
        GENRE_CATEGORIES
    ).order_by(
        GENRE_CATEGORIES.display_order.asc()
    ).all()

    return categories


# ==========================================
# GET SINGLE CATEGORY
# ==========================================

@router.get(
    "/{category_id}",
    response_model=GenreCategoryResponse
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    category = db.query(
        GENRE_CATEGORIES
    ).filter(
        GENRE_CATEGORIES.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre category not found"
        )

    return category


# ==========================================
# UPDATE CATEGORY
# ==========================================

@router.put(
    "/{category_id}",
    response_model=GenreCategoryResponse
)
def update_category(
    category_id: int,
    data: GenreCategoryUpdate,
    db: Session = Depends(get_db)
):

    category = db.query(
        GENRE_CATEGORIES
    ).filter(
        GENRE_CATEGORIES.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre category not found"
        )

    # Check duplicate slug
    if data.slug and data.slug != category.slug:

        existing_category = db.query(
            GENRE_CATEGORIES
        ).filter(
            GENRE_CATEGORIES.slug == data.slug,
            GENRE_CATEGORIES.id != category_id
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists"
            )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


# ==========================================
# DELETE CATEGORY
# ==========================================

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    category = db.query(
        GENRE_CATEGORIES
    ).filter(
        GENRE_CATEGORIES.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre category not found"
        )

    db.delete(category)
    db.commit()

    return None

