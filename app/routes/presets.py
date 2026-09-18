from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.preset_categories import PRESETS, PRESET_CATEGORIES
from app.models.user import User
from app.schemas.presets import (
    PresetCreate, PresetUpdate, PresetResponse,
    PresetCategoryCreate, PresetCategoryResponse
)
from app.schemas.pagination import PaginatedResponse
from app.utils.pagination import paginate, pagination_params

router = APIRouter(prefix="/presets", tags=["Presets"])

# ---------- Categories ----------
@router.post("/categories", response_model=PresetCategoryResponse)
def create_category(payload: PresetCategoryCreate, db: Session = Depends(get_db)):
    category = PRESET_CATEGORIES(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.get("/categories", response_model=PaginatedResponse[PresetCategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    query = db.query(PRESET_CATEGORIES).order_by(PRESET_CATEGORIES.display_order)
    return paginate(query, **pagination)

@router.get("/categories/{category_id}", response_model=PresetCategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
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

@router.get("/", response_model=PaginatedResponse[PresetResponse])
def list_presets(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    _current_user: User = Depends(get_current_user),
):
    query = db.query(PRESETS)
    if category_id:
        query = query.filter(PRESETS.category_id == category_id)
    return paginate(query, **pagination)

@router.get("/{preset_id}", response_model=PresetResponse)
def get_preset(
    preset_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
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

@router.put("/{preset_id}/pack/{pack_id}", response_model=PresetResponse)
def assign_preset_to_pack(preset_id: int, pack_id: int, db: Session = Depends(get_db)):
    from app.models.packs import Pack

    preset = db.query(PRESETS).filter(PRESETS.id == preset_id).first()
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    pack = db.query(Pack).filter(Pack.id == pack_id).first()
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")

    preset.pack_id = pack_id
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