from sqlalchemy import String,ForeignKey, Column,Integer
from app.core.database import Base
from sqlalchemy.orm import relationship

class PRESET_CATEGORIES(Base):
    __tablename__ = "preset_categories"

    id = Column(Integer, primary_key=True , nullable=False)
    name = Column(String, nullable=False)
    display_order = Column(Integer)

    presets = relationship("PRESETS", back_populates="category")

class PRESETS (Base):
    __tablename__ = "presets"

    id = Column(Integer, primary_key=True , nullable=False , index=True)
    category_id = Column(Integer,ForeignKey("preset_categories.id"))
    name = Column(String,nullable=False)
    synth_type = Column(String, nullable=False)
    file_url = Column(String)
    compatible_daw = Column(String)

    category = relationship("PRESET_CATEGORIES", back_populates="presets")