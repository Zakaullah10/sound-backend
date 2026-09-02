from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.label import Label
from app.schemas.labels import (
    LabelCreate,
    LabelResponse
)


router = APIRouter(
    prefix="/labels",
    tags=["Labels"]
)


@router.post(
    "/",
    response_model=LabelResponse
)
def create_label(
    label: LabelCreate,
    db: Session = Depends(get_db)
):

    existing_label = (
        db.query(Label)
        .filter(Label.name == label.name)
        .first()
    )

    if existing_label:
        raise HTTPException(
            status_code=400,
            detail="Label already exists"
        )

    new_label = Label(
        name=label.name,
        verified=label.verified
    )

    db.add(new_label)
    db.commit()
    db.refresh(new_label)

    return new_label


@router.get(
    "/",
    response_model=list[LabelResponse]
)
def get_labels(
    db: Session = Depends(get_db)
):

    return db.query(Label).all()


@router.get(
    "/{label_id}",
    response_model=LabelResponse
)
def get_label(
    label_id: int,
    db: Session = Depends(get_db)
):

    label = (
        db.query(Label)
        .filter(Label.id == label_id)
        .first()
    )

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    return label


@router.delete(
    "/{label_id}"
)


def delete_label(
    label_id: int,
    db: Session = Depends(get_db)
):

    label = (
        db.query(Label)
        .filter(Label.id == label_id)
        .first()
    )

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    db.delete(label)
    db.commit()

    return {
        "message": "Label deleted successfully"
    }



@router.get("/{label_id}/packs")
def get_packs_by_label(
    label_id: int,
    db: Session = Depends(get_db)
):
    label = db.query(Label).filter(Label.id == label_id).first()

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    return label.packs