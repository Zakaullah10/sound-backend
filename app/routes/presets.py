from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.preset_categories import PRESETS, PRESET_CATEGORIES
from app.schemas.presets import (
    PresetCreate, PresetUpdate, PresetResponse,
    PresetCategoryCreate, PresetCategoryResponse
)

router = APIRouter(prefix="/presets", tags=["Presets"])

# ---------- Categories ----------
@router.post("/categories", response_model=PresetCategoryResponse)
def create_category(payload: PresetCategoryCreate, db: Session = Depends(get_db)):
    category = PRESET_CATEGORIES(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=List[PresetCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(PRESET_CATEGORIES).order_by(PRESET_CATEGORIES.display_order).all()

@router.get("/categories/{category_id}", response_model=PresetCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(PRESET_CATEGORIES).filter(PRESET_CATEGORIES.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(PRESET_CATEGORIES).filter(PRESET_CATEGORIES.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"detail": "Category deleted"}

# ---------- Presets ----------
@router.post("/", response_model=PresetResponse)
def create_preset(payload: PresetCreate, db: Session = Depends(get_db)):
    preset = PRESETS(**payload.dict())
    db.add(preset)
    db.commit()
    db.refresh(preset)
    return preset

@router.get("/", response_model=List[PresetResponse])
def list_presets(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(PRESETS)
    if category_id:
        query = query.filter(PRESETS.category_id == category_id)
    return query.all()

@router.get("/{preset_id}", response_model=PresetResponse)
def get_preset(preset_id: int, db: Session = Depends(get_db)):
    preset = db.query(PRESETS).filter(PRESETS.id == preset_id).first()
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset

@router.put("/{preset_id}", response_model=PresetResponse)
def update_preset(preset_id: int, payload: PresetUpdate, db: Session = Depends(get_db)):
    preset = db.query(PRESETS).filter(PRESETS.id == preset_id).first()
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    for key, value in payload.dict().items():
        setattr(preset, key, value)
    db.commit()
    db.refresh(preset)
    return preset

@router.delete("/{preset_id}")
def delete_preset(preset_id: int, db: Session = Depends(get_db)):
    preset = db.query(PRESETS).filter(PRESETS.id == preset_id).first()
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    db.delete(preset)
    db.commit()
    return {"detail": "Preset deleted"}