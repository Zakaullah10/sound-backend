from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.packs import Pack
from app.models.songs import SONGS

from app.schemas.songs import (
    SongCreate,
    SongResponse
)


router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


@router.post(
    "/packs/{pack_id}",
    response_model=SongResponse
)
def create_song(
    pack_id: int,
    song: SongCreate,
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

    new_song = SONGS(
        pack_id=pack_id,
        title=song.title,
        audio_url=song.audio_url,
        duration=song.duration
    )

    db.add(new_song)

    # Update cached track count
    pack.track_count += 1

    db.commit()
    db.refresh(new_song)

    return new_song


@router.get(
    "/packs/{pack_id}",
    response_model=list[SongResponse]
)
def get_pack_songs(
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

    return (
        db.query(SONGS)
        .filter(SONGS.pack_id == pack_id)
        .all()
    )


@router.get(
    "/{song_id}",
    response_model=SongResponse
)
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):

    song = (
        db.query(SONGS)
        .filter(SONGS.id == song_id)
        .first()
    )

    if not song:
        raise HTTPException(
            status_code=404,
            detail="Song not found"
        )

    return song