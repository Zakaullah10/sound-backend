# from sqlalchemy import Column , Integer,String,ForeignKey,Boolean
# from app.core.database import Base
# from sqlalchemy.orm import relationship


# class GENRE_CATEGORIES(Base):
#     __tablename__ = "genre_categories"

#     id = Column(Integer , primary_key=True , index=True)
#     name = Column(String , nullable=False)
#     slug = Column(String, nullable=False)
#     display_order = Column(Integer)

#     genres = relationship("GENRE", back_populates="category")


# class GENRE (Base):

#     __tablename__ = "genre"

#     id = Column(Integer, primary_key=True ,index=True )
#     category_id = Column(Integer,ForeignKey("genre_categories.id"))
#     name = Column (String,nullable=False)
#     slug = Column(String,nullable=False)
#     is_featured = Column(Boolean,default=False)
#     display_order = Column(Integer)

#        # Relationship
#     packs  = relationship("PACK", back_populates="genre")
#     category = relationship("GENRE_CATEGORIES", back_populates="genres")

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class GENRE_CATEGORIES(Base):
    __tablename__ = "genre_categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    slug = Column(
        String,
        nullable=False
    )

    display_order = Column(Integer)

    genres = relationship(
        "GENRE",
        back_populates="category"
    )


class GENRE(Base):
    __tablename__ = "genre"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey("genre_categories.id")
    )

    name = Column(
        String,
        nullable=False
    )

    slug = Column(
        String,
        nullable=False
    )

    is_featured = Column(
        Boolean,
        default=False
    )

    display_order = Column(Integer)

    # Relationships

    packs = relationship(
        "Pack",
        back_populates="genre"
    )

    category = relationship(
        "GENRE_CATEGORIES",
        back_populates="genres"
    )

    labels = relationship(
        "Label",
        secondary="label_genres",
        back_populates="genres"
    )