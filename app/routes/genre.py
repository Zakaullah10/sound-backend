from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.genre_categories import GENRE
from app.models.genre_categories import GENRE_CATEGORIES

from app.schemas.genre import (
    GenreCreate,
    GenreUpdate,
    GenreResponse,
)


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


# --------------------------------
# CREATE GENRE
# --------------------------------

@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED
)
def create_genre(
    data: GenreCreate,
    db: Session = Depends(get_db)
):

    # Check category if provided
    if data.category_id:

        category = db.query(GENRE_CATEGORIES).filter(
            GENRE_CATEGORIES.id == data.category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Genre category not found"
            )

    # Check duplicate slug
    existing_genre = db.query(GENRE).filter(
        GENRE.slug == data.slug
    ).first()

    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="Genre slug already exists"
        )

    genre = GENRE(
        category_id=data.category_id,
        name=data.name,
        slug=data.slug,
        is_featured=data.is_featured,
        display_order=data.display_order
    )

    db.add(genre)
    db.commit()
    db.refresh(genre)

    return genre


# --------------------------------
# GET ALL GENRES
# --------------------------------

@router.get(
    "/",
    response_model=list[GenreResponse]
)
def get_genres(
    db: Session = Depends(get_db)
):

    genres = db.query(GENRE).order_by(
        GENRE.display_order.asc()
    ).all()

    return genres


# --------------------------------
# GET FEATURED GENRES
# --------------------------------

@router.get(
    "/featured",
    response_model=list[GenreResponse]
)
def get_featured_genres(
    db: Session = Depends(get_db)
):

    genres = db.query(GENRE).filter(
        GENRE.is_featured == True
    ).order_by(
        GENRE.display_order.asc()
    ).all()

    return genres


# --------------------------------
# GET GENRES BY CATEGORY
# --------------------------------

@router.get(
    "/category/{category_id}",
    response_model=list[GenreResponse]
)
def get_genres_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    category = db.query(GENRE_CATEGORIES).filter(
        GENRE_CATEGORIES.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Genre category not found"
        )

    genres = db.query(GENRE).filter(
        GENRE.category_id == category_id
    ).order_by(
        GENRE.display_order.asc()
    ).all()

    return genres


# --------------------------------
# GET SINGLE GENRE
# --------------------------------

@router.get(
    "/{genre_id}",
    response_model=GenreResponse
)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):

    genre = db.query(GENRE).filter(
        GENRE.id == genre_id
    ).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    return genre


# --------------------------------
# UPDATE GENRE
# --------------------------------

@router.put(
    "/{genre_id}",
    response_model=GenreResponse
)
def update_genre(
    genre_id: int,
    data: GenreUpdate,
    db: Session = Depends(get_db)
):

    genre = db.query(GENRE).filter(
        GENRE.id == genre_id
    ).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    # Check category
    if data.category_id is not None:

        category = db.query(GENRE_CATEGORIES).filter(
            GENRE_CATEGORIES.id == data.category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Genre category not found"
            )

    # Check slug
    if data.slug and data.slug != genre.slug:

        existing_genre = db.query(GENRE).filter(
            GENRE.slug == data.slug,
            GENRE.id != genre_id
        ).first()

        if existing_genre:
            raise HTTPException(
                status_code=400,
                detail="Genre slug already exists"
            )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(genre, key, value)

    db.commit()
    db.refresh(genre)

    return genre


# --------------------------------
# DELETE GENRE
# --------------------------------

@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):

    genre = db.query(GENRE).filter(
        GENRE.id == genre_id
    ).first()

    if not genre:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    db.delete(genre)
    db.commit()

    return None

