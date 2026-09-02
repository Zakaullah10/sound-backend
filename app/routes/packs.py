from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.packs import Pack
from app.models.label import Label

from app.schemas.packs import (
    PackCreate,
    PackResponse,
    PackDetailResponse
)


router = APIRouter(
    prefix="/packs",
    tags=["Packs"]
)


@router.post(
    "/",
    response_model=PackResponse
)
def create_pack(
    pack: PackCreate,
    db: Session = Depends(get_db)
):

    # Find labels
    labels = []

    if pack.label_ids:

        labels = (
            db.query(Label)
            .filter(Label.id.in_(pack.label_ids))
            .all()
        )

        if len(labels) != len(set(pack.label_ids)):
            raise HTTPException(
                status_code=404,
                detail="One or more labels not found"
            )

    # Create pack
    new_pack = Pack(
        title=pack.title,
        description=pack.description,
        cover_image=pack.cover_image,
        price=pack.price,
        is_free=pack.is_free,
        status=pack.status,
        genre_id=pack.genre_id
    )

    # Assign multiple labels
    new_pack.labels = labels

    db.add(new_pack)
    db.commit()
    db.refresh(new_pack)

    return new_pack


@router.get(
    "/",
    response_model=list[PackResponse]
)
def get_packs(
    db: Session = Depends(get_db)
):

    return db.query(Pack).all()


@router.get(
    "/{pack_id}",
    response_model=PackDetailResponse
)
def get_pack(
    pack_id: int,
    db: Session = Depends(get_db)
):

    pack = (
        db.query(Pack)
        .filter(Pack.id == pack_id)
        .first()
    )

    if not pack:
        raise HTTPException(
            status_code=404,
            detail="Pack not found"
        )

    return pack


@router.delete(
    "/{pack_id}"
)
def delete_pack(
    pack_id: int,
    db: Session = Depends(get_db)
):

    pack = (
        db.query(Pack)
        .filter(Pack.id == pack_id)
        .first()
    )

    if not pack:
        raise HTTPException(
            status_code=404,
            detail="Pack not found"
        )

    db.delete(pack)
    db.commit()

    return {
        "message": "Pack deleted successfully"
    }