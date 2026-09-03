from pydantic import BaseModel
from typing import Optional, List

# ---- Category ----
class PresetCategoryBase(BaseModel):
    name: str
    display_order: Optional[int] = None

class PresetCategoryCreate(PresetCategoryBase):
    pass

class PresetCategoryResponse(PresetCategoryBase):
    id: int
    class Config:
        from_attributes = True

# ---- Preset ----
class PresetBase(BaseModel):
    name: str
    synth_type: str
    file_url: Optional[str] = None
    compatible_daw: Optional[str] = None
    category_id: Optional[int] = None
    pack_id: Optional[int] = None   # ye zaroor hona chahiye

class PresetCreate(PresetBase):
    pass

class PresetUpdate(PresetBase):
    pass

class PresetResponse(PresetBase):
    id: int
    class Config:
        from_attributes = True