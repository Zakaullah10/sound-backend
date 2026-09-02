# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     Numeric,
#     Boolean,
#     ForeignKey,
#     TIMESTAMP,
#     func,
# )
# from sqlalchemy.orm import relationship

# from app.core.database import Base


# class SONGS(Base):
#     __tablename__ = "songs"

#     id = Column(Integer, primary_key=True, index=True)

#     pack_id = Column(
#         Integer,
#         ForeignKey("packs.id", ondelete="CASCADE"),
#         nullable=False
#     )
#     title = Column(String(150), nullable=False)
#     file_url = Column(Text, nullable=False)

#     preview_url  = Column(Text)
#     duration_seconds = Column(Integer)

#     bpm  = Column(Integer, default=0)
#     musical_key  = Column(String)
#     file_format  =  Column(String)
#     position   =  Column(Integer)

#     created_at = Column(TIMESTAMP, server_default=func.now())

#     # Relationships
#     packs = relationship("PACK", back_populates="songs")


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.core.database import Base


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

    packs = relationship(
        "Pack",
        back_populates="songs"
    )