from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(Integer, primary_key=True, index=True)

    payment_id = Column(
        Integer,
        ForeignKey("payments.id", ondelete="CASCADE"),
        nullable=False
    )

    old_status = Column(String(20))
    new_status = Column(String(20), nullable=False)

    note = Column(Text)     # e.g. "Payment failed due to insufficient balance"

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    payment = relationship("Payment", back_populates="history")