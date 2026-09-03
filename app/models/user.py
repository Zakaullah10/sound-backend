from sqlalchemy import Column, Integer, String,TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(TIMESTAMP, nullable=True)

    # Relationships
    payments = relationship("Payment", back_populates="user")
    notification_setting = relationship("NotificationSetting", back_populates="user")  # 👈 ye line add karein
    payment_methods = relationship(
    "PaymentMethod",
    back_populates="user",
    cascade="all, delete-orphan"
)