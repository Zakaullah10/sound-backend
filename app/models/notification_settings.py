from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base  # <-- ye line apne actual import path se replace karein

class NotificationSetting(Base):
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)  # "users" ki jagah "user"
    settings = Column(JSON, nullable=False, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="notification_setting")