# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     Numeric,
#     Boolean,
#     ForeignKey,
#     TIMESTAMP,
#     Table,
#     func,
# )
# from sqlalchemy.orm import relationship

# from app.core.database import Base


# pack_tags = Table(
#     "pack_tags",
#     Base.metadata,

#     Column(
#         "pack_id",
#         Integer,
#         ForeignKey("packs.id", ondelete="CASCADE"),
#         primary_key=True
#     ),

#     Column(
#         "tag_id",
#         Integer,
#         ForeignKey("instrument_tags.id", ondelete="CASCADE"),
#         primary_key=True
#     )
# )


# class Pack(Base):
#     __tablename__ = "packs"

#     id = Column(Integer, primary_key=True, index=True)

#     genre_id = Column(
#         Integer,
#         ForeignKey("genres.id")
#     )

#     title = Column(String(150), nullable=False)
#     cover_image = Column(Text)
#     description = Column(Text)

#     price = Column(Numeric(10, 2), default=0)
#     is_free = Column(Boolean, default=False)

#     status = Column(String(20), default="draft")

#     download_count = Column(Integer, default=0)
#     favorite_count = Column(Integer, default=0)
#     track_count = Column(Integer, default=0)

#     released_at = Column(TIMESTAMP)
#     created_at = Column(TIMESTAMP, server_default=func.now())

#     # Relationships
#     labels = relationship(
#         "Label",
#         secondary="label_packs",
#         back_populates="packs"
#     )

#     genre = relationship(
#         "Genre",
#         back_populates="packs"
#     )

#     songs = relationship(
#         "SONGS",
#         back_populates="packs"
#     )

#     tags = relationship(
#         "InstrumentTag",
#         secondary=pack_tags,
#         back_populates="packs"
#     )



from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    Table,
    func,
)
from sqlalchemy.orm import relationship

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


class Pack(Base):
    __tablename__ = "packs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    genre_id = Column(
        Integer,
        ForeignKey("genre.id")
    )

    title = Column(
        String(150),
        nullable=False
    )

    cover_image = Column(Text)

    description = Column(Text)

    price = Column(
        Numeric(10, 2),
        default=0
    )

    is_free = Column(
        Boolean,
        default=False
    )

    status = Column(
        String(20),
        default="draft"
    )

    download_count = Column(
        Integer,
        default=0
    )

    favorite_count = Column(
        Integer,
        default=0
    )

    track_count = Column(
        Integer,
        default=0
    )

    released_at = Column(TIMESTAMP)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    # Label ↔ Pack = Many-to-Many
    labels = relationship(
        "Label",
        secondary="label_packs",
        back_populates="packs"
    )

    # Genre → Pack = One-to-Many
    genre = relationship(
        "GENRE",
        back_populates="packs"
    )

    # Pack → Songs = One-to-Many
    songs = relationship(
        "SONGS",
        back_populates="packs"
    )

    # Pack ↔ Instrument Tags = Many-to-Many
    tags = relationship(
        "INSTRUMENT_TAGS",
        secondary=pack_tags,
        back_populates="packs"
    )
    presets = relationship("PRESETS", back_populates="pack")