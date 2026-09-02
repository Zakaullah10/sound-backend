from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.instruments import INSTRUMENT_TAGS, INSTRUMENT_CATEGORIES
from app.schemas.instruments import (
    InstrumentTagCreate, InstrumentTagUpdate, InstrumentTagResponse,
    InstrumentCategoryCreate, InstrumentCategoryResponse
)

router = APIRouter(prefix="/instruments", tags=["Instruments"])

# ---------- Categories ----------
@router.post("/categories", response_model=InstrumentCategoryResponse)
def create_category(payload: InstrumentCategoryCreate, db: Session = Depends(get_db)):
    category = INSTRUMENT_CATEGORIES(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=List[InstrumentCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(INSTRUMENT_CATEGORIES).order_by(INSTRUMENT_CATEGORIES.display_order).all()

@router.get("/categories/{category_id}", response_model=InstrumentCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
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

@router.get("/", response_model=List[InstrumentTagResponse])
def list_instruments(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(INSTRUMENT_TAGS)
    if category_id:
        query = query.filter(INSTRUMENT_TAGS.category_id == category_id)
    return query.all()

@router.get("/{instrument_id}", response_model=InstrumentTagResponse)
def get_instrument(instrument_id: int, db: Session = Depends(get_db)):
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