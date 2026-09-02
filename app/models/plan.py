from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)          # e.g. "Pro Plan"
    description = Column(String(255))

    price = Column(Numeric(10, 2), nullable=False, default=0)
    duration_days = Column(Integer, nullable=False)      # e.g. 30, 365

    stripe_price_id = Column(String(150), nullable=False)   # Stripe Dashboard se milega
    stripe_product_id = Column(String(150))

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    payments = relationship("Payment", back_populates="plan")