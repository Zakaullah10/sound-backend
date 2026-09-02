import stripe
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.payment import Payment
from app.services.stripe_service import update_payment_status

stripe.api_key = settings.STRIPE_SECRET_KEY


def handle_stripe_webhook(payload: bytes, sig_header: str, db: Session):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        raise ValueError("Invalid webhook signature")

    event_type = event["type"]
    data = event["data"]["object"].to_dict()   # <-- yeh line add ki hai

    if event_type == "checkout.session.completed":
        session_id = data.get("id")
        subscription_id = data.get("subscription")

        payment = db.query(Payment).filter(
            Payment.stripe_checkout_session_id == session_id
        ).first()

        if payment:
            payment.stripe_subscription_id = subscription_id
            update_payment_status(db, payment, "success", note="Checkout completed")

    elif event_type == "invoice.payment_failed":
        subscription_id = data.get("subscription")
        payment = db.query(Payment).filter(
            Payment.stripe_subscription_id == subscription_id
        ).first()

        if payment:
            update_payment_status(db, payment, "failed", note="Invoice payment failed")

    elif event_type == "customer.subscription.deleted":
        subscription_id = data.get("id")
        payment = db.query(Payment).filter(
            Payment.stripe_subscription_id == subscription_id
        ).first()

        if payment:
            update_payment_status(db, payment, "cancelled", note="Subscription cancelled")

    return {"status": "success"}