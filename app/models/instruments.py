# from sqlalchemy import Column , String,Integer,ForeignKey,Boolean
# from sqlalchemy.orm import relationship
# from app.core.database import Base
# from app.models.packs import pack_tags


# class INSTRUMENT_CATEGORIES(Base):
#     __tablename__ = "instrument_categories"

#     id = Column(Integer, primary_key=True , index=True)
#     name = Column(String, nullable=False)
#     slug = Column(String, nullable=False)
#     display_order = Column(Integer)

#     instrument = relationship("INSTRUMENT_TAGS", back_populates="category")



# class INSTRUMENT_TAGS(Base):
#     __tablename__ = "instrument_tags"

#     id = Column(Integer,primary_key=True , index=True)
#     category_id = Column(Integer,ForeignKey("instrument_categories.id"))
#     name = Column(String, nullable=False )
#     slug = Column(String)
#     is_featured = Column(Boolean, default=False)
#     display_order = Column(Integer)

#     category = relationship("INSTRUMENT_CATEGORIES", back_populates="instrument")
#     packs = relationship(
#         "Pack",
#         secondary=pack_tags,
#         back_populates="tags"
#     )

from sqlalchemy import Column , String,Integer,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.packs import pack_tags
from app.models.songs import song_tags


class INSTRUMENT_CATEGORIES(Base):
    __tablename__ = "instrument_categories"

    id = Column(Integer, primary_key=True , index=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    display_order = Column(Integer)

    instrument = relationship("INSTRUMENT_TAGS", back_populates="category")


class INSTRUMENT_TAGS(Base):
    __tablename__ = "instrument_tags"

    id = Column(Integer,primary_key=True , index=True)
    category_id = Column(Integer,ForeignKey("instrument_categories.id"))
    name = Column(String, nullable=False )
    slug = Column(String)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer)

    category = relationship("INSTRUMENT_CATEGORIES", back_populates="instrument")

    packs = relationship(
        "Pack",
        secondary=pack_tags,
        back_populates="tags"
    )

    # naya: Song ↔ Instrument Tags
    songs = relationship(
        "SONGS",
        secondary=song_tags,
        back_populates="tags"
    )