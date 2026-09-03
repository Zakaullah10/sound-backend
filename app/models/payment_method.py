from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    stripe_payment_method_id = Column(
        String(200),
        unique=True,
        nullable=False
    )

    type = Column(
        String(50),
        nullable=False,
        default="card"
    )

    card_brand = Column(String(50), nullable=True)
    card_last4 = Column(String(4), nullable=True)

    card_exp_month = Column(Integer, nullable=True)
    card_exp_year = Column(Integer, nullable=True)

    is_default = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="payment_methods"
    )

    payments = relationship(
        "Payment",
        back_populates="payment_method"
    )