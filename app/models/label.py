# from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
# from sqlalchemy.orm import relationship

# from app.core.database import Base
# from app.models.label_genre import label_genres


# label_packs = Table(
#     "label_packs",
#     Base.metadata,

#     Column(
#         "label_id",
#         Integer,
#         ForeignKey("labels.id", ondelete="CASCADE"),
#         primary_key=True
#     ),

#     Column(
#         "pack_id",
#         Integer,
#         ForeignKey("packs.id", ondelete="CASCADE"),
#         primary_key=True
#     )
# )


# class Label(Base):
#     __tablename__ = "labels"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     verified = Column(Boolean, default=False)

#     genres = relationship(
#         "Genre",
#         secondary=label_genres,
#         back_populates="labels"
#     )

#     packs = relationship(
#         "Pack",
#         secondary=label_packs,
#         back_populates="labels"
#     )


from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.label_genre import label_genres


label_packs = Table(
    "label_packs",
    Base.metadata,

    Column(
        "label_id",
        Integer,
        ForeignKey("labels.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "pack_id",
        Integer,
        ForeignKey("packs.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    verified = Column(
        Boolean,
        default=False
    )

    genres = relationship(
    "GENRE",
    secondary=label_genres,
    back_populates="labels"
    )

    packs = relationship(
        "Pack",
        secondary=label_packs,
        back_populates="labels"
    )