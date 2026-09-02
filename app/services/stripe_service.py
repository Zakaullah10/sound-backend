import stripe
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.plan import Plan
from app.models.user import User
from app.models.payment import Payment
from app.models.payment_history import PaymentHistory

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(db: Session, user: User, plan_id: int) -> str:
    plan = db.query(Plan).filter(Plan.id == plan_id, Plan.is_active == True).first()
    if not plan:
      raise ValueError("Plan not found or inactive")

    # Pending payment record pehle hi bana lete hain
    payment = Payment(
        user_id=user.id,
        plan_id=plan.id,
        amount=plan.price,
        currency="usd",
        status="pending",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        customer_email=user.email,
        line_items=[{
            "price": plan.stripe_price_id,
            "quantity": 1,
        }],
        success_url=settings.FRONTEND_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.FRONTEND_CANCEL_URL,
        metadata={
            "payment_id": str(payment.id),
            "user_id": str(user.id),
            "plan_id": str(plan.id),
        },
    )

    # Session id save kar dete hain payment record mein
    payment.stripe_checkout_session_id = session.id
    db.commit()

    return session.url


def update_payment_status(db: Session, payment: Payment, new_status: str, note: str = None):
    old_status = payment.status
    payment.status = new_status
    db.add(payment)

    history = PaymentHistory(
        payment_id=payment.id,
        old_status=old_status,
        new_status=new_status,
        note=note,
    )
    db.add(history)
    db.commit()