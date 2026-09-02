from sqlalchemy import Table, Column, Integer, ForeignKey

from app.core.database import Base


pack_tags = Table(
    "pack_tags",
    Base.metadata,

    Column(
        "pack_id",
        Integer,
        ForeignKey(
            "packs.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    Column(
        "tag_id",
        Integer,
        ForeignKey(
            "instrument_tags.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)