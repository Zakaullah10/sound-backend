# # from sqlalchemy import (
# #     Column,
# #     Integer,
# #     String,
# #     Text,
# #     Numeric,
# #     Boolean,
# #     ForeignKey,
# #     TIMESTAMP,
# #     func,
# # )
# # from sqlalchemy.orm import relationship

# # from app.core.database import Base


# # class SONGS(Base):
# #     __tablename__ = "songs"

# #     id = Column(Integer, primary_key=True, index=True)

# #     pack_id = Column(
# #         Integer,
# #         ForeignKey("packs.id", ondelete="CASCADE"),
# #         nullable=False
# #     )
# #     title = Column(String(150), nullable=False)
# #     file_url = Column(Text, nullable=False)

# #     preview_url  = Column(Text)
# #     duration_seconds = Column(Integer)

# #     bpm  = Column(Integer, default=0)
# #     musical_key  = Column(String)
# #     file_format  =  Column(String)
# #     position   =  Column(Integer)

# #     created_at = Column(TIMESTAMP, server_default=func.now())

# #     # Relationships
# #     packs = relationship("PACK", back_populates="songs")


# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     ForeignKey
# )
# from sqlalchemy.orm import relationship

# from app.core.database import Base


# class SONGS(Base):
#     __tablename__ = "songs"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     pack_id = Column(
#         Integer,
#         ForeignKey(
#             "packs.id",
#             ondelete="CASCADE"
#         ),
#         nullable=False
#     )

#     title = Column(
#         String(150),
#         nullable=False
#     )

#     audio_url = Column(Text)

#     duration = Column(Integer)

#     packs = relationship(
#         "Pack",
#         back_populates="songs"
#     )


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship

from app.core.database import Base


song_tags = Table(
    "song_tags",
    Base.metadata,

    Column(
        "song_id",
        Integer,
        ForeignKey("songs.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "tag_id",
        Integer,
        ForeignKey("instrument_tags.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class SONGS(Base):
    __tablename__ = "songs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pack_id = Column(
        Integer,
        ForeignKey(
            "packs.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    title = Column(
        String(150),
        nullable=False
    )

    audio_url = Column(Text)

    duration = Column(Integer)

    key = Column(String(10))       # e.g. "C Major" — image mein Key column dikha
    bpm = Column(Integer)          # image mein BPM column dikha

    packs = relationship(
        "Pack",
        back_populates="songs"
    )

    # Song ↔ Instrument Tags = Many-to-Many (naya)
    tags = relationship(
        "INSTRUMENT_TAGS",
        secondary=song_tags,
        back_populates="songs"
    )