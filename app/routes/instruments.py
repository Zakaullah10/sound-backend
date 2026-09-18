from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.instruments import INSTRUMENT_TAGS, INSTRUMENT_CATEGORIES
from app.models.user import User
from app.schemas.instruments import (
    InstrumentTagCreate, InstrumentTagUpdate, InstrumentTagResponse,
    InstrumentCategoryCreate, InstrumentCategoryResponse
)
from app.schemas.pagination import PaginatedResponse
from app.utils.pagination import paginate, pagination_params

router = APIRouter(prefix="/instruments", tags=["Instruments"])

# ---------- Categories ----------
@router.post("/categories", response_model=InstrumentCategoryResponse)
def create_category(payload: InstrumentCategoryCreate, db: Session = Depends(get_db)):
    category = INSTRUMENT_CATEGORIES(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=PaginatedResponse[InstrumentCategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    query = db.query(INSTRUMENT_CATEGORIES).order_by(INSTRUMENT_CATEGORIES.display_order)
    return paginate(query, **pagination)

@router.get("/categories/{category_id}", response_model=InstrumentCategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    category = db.query(INSTRUMENT_CATEGORIES).filter(INSTRUMENT_CATEGORIES.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(INSTRUMENT_CATEGORIES).filter(INSTRUMENT_CATEGORIES.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}

# ---------- Instrument Tags ----------
@router.post("/", response_model=InstrumentTagResponse)
def create_instrument(payload: InstrumentTagCreate, db: Session = Depends(get_db)):
    instrument = INSTRUMENT_TAGS(**payload.dict())
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument

@router.get("/", response_model=PaginatedResponse[InstrumentTagResponse])
def list_instruments(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    query = db.query(INSTRUMENT_TAGS)
    if category_id:
        query = query.filter(INSTRUMENT_TAGS.category_id == category_id)
    return paginate(query, **pagination)

@router.get("/{instrument_id}", response_model=InstrumentTagResponse)
def get_instrument(
    instrument_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    instrument = db.query(INSTRUMENT_TAGS).filter(INSTRUMENT_TAGS.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument

@router.put("/{instrument_id}", response_model=InstrumentTagResponse)
def update_instrument(instrument_id: int, payload: InstrumentTagUpdate, db: Session = Depends(get_db)):
    instrument = db.query(INSTRUMENT_TAGS).filter(INSTRUMENT_TAGS.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    for key, value in payload.dict().items():
        setattr(instrument, key, value)
    db.commit()
    db.refresh(instrument)
    return instrument

@router.delete("/{instrument_id}")
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(INSTRUMENT_TAGS).filter(INSTRUMENT_TAGS.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    db.delete(instrument)
    db.commit()
    return {"detail": "Instrument deleted"}