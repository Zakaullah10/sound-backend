from pydantic import BaseModel
from typing import Optional


class SongCreate(BaseModel):
    title: str
    audio_url: Optional[str] = None
    duration: Optional[int] = None


class SongResponse(BaseModel):
    id: int
    pack_id: int
    title: str
    audio_url: Optional[str]
    duration: Optional[int]

    class Config:
        from_attributes = True