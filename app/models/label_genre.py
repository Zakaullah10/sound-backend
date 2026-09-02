from sqlalchemy import Table, Column, Integer, ForeignKey

from app.core.database import Base


label_genres = Table(
    "label_genres",
    Base.metadata,

    Column(
        "label_id",
        Integer,
        ForeignKey(
            "labels.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    Column(
        "genre_id",
        Integer,
        ForeignKey(
            "genre.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)