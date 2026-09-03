from pydantic import BaseModel
from typing import Optional, List


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SongBase(BaseModel):
    title: str
    audio_url: Optional[str] = None
    duration: Optional[int] = None
    key: Optional[str] = None      # naya — model mein add kiya tha
    bpm: Optional[int] = None      # naya — model mein add kiya tha


class SongCreate(SongBase):
    pass


class SongResponse(SongBase):
    id: int
    pack_id: int
    tags: List[TagResponse] = []   # relationship test karne ke liye

    class Config:
        from_attributes = True