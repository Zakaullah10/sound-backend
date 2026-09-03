from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    TIMESTAMP,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    plan_id = Column(
        Integer,
        ForeignKey("plans.id"),
        nullable=False
    )

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="USD")

    payment_method_id = Column(
    Integer,
    ForeignKey("payment_methods.id", ondelete="SET NULL"),
    nullable=True
     )
    transaction_id = Column(String(150), unique=True)   # gateway se aane wala id

    stripe_checkout_session_id = Column(String(200), unique=True, nullable=True)
    stripe_payment_intent_id = Column(String(200), unique=True, nullable=True)
    stripe_subscription_id = Column(String(200), unique=True, nullable=True)

    status = Column(String(20), default="pending")   # pending, success, failed, refunded

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")
    plan = relationship("Plan", back_populates="payments")
    history = relationship(
        "PaymentHistory",
        back_populates="payment",
        cascade="all, delete-orphan"
    )
    payment_method = relationship(
    "PaymentMethod",
    back_populates="payments" 
    )