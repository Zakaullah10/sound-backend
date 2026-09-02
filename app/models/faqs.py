from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    display_order = Column(Integer)
    is_active = Column(Boolean, default=True)