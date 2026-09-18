from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.label import Label
from app.models.packs import Pack
from app.models.user import User
from app.schemas.labels import (
    LabelCreate,
    LabelResponse
)
from app.schemas.packs import PackResponse
from app.schemas.pagination import PaginatedResponse
from app.utils.pagination import paginate, pagination_params


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
    response_model=PaginatedResponse[LabelResponse]
)
def get_labels(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    query = db.query(Label).options(selectinload(Label.genres))
    return paginate(query, **pagination)

@router.get(
    "/{label_id}",
    response_model=LabelResponse
)
def get_label(
    label_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):

    label = (
        db.query(Label)
        .options(selectinload(Label.genres))
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



@router.get(
    "/{label_id}/packs",
    response_model=PaginatedResponse[PackResponse],
)
def get_packs_by_label(
    label_id: int,
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    label = db.query(Label).filter(Label.id == label_id).first()

    if not label:
        raise HTTPException(
            status_code=404,
            detail="Label not found"
        )

    query = (
        db.query(Pack)
        .join(Pack.labels)
        .filter(Label.id == label_id)
    )
    return paginate(query, **pagination)