import stripe

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.dependencies.auth import get_current_user
from app.models.payment_method import PaymentMethod

from app.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodResponse
)


stripe.api_key = settings.STRIPE_SECRET_KEY


router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"]
)


# =========================================================
# ADD PAYMENT METHOD
# =========================================================

@router.post(
    "",
    response_model=PaymentMethodResponse
)
def add_payment_method(
    data: PaymentMethodCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # TODO:
    # JWT se current user lena hai
    user_id = current_user.id

    # -----------------------------------------------------
    # Check if payment method already exists
    # -----------------------------------------------------

    existing = db.query(PaymentMethod).filter(
        PaymentMethod.stripe_payment_method_id
        == data.stripe_payment_method_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Payment method already exists"
        )

    try:

        # -------------------------------------------------
        # Get PaymentMethod from Stripe
        # -------------------------------------------------

        stripe_pm = stripe.PaymentMethod.retrieve(
            data.stripe_payment_method_id
        )

        # -------------------------------------------------
        # Only card payment methods
        # -------------------------------------------------

        if stripe_pm.type != "card":

            raise HTTPException(
                status_code=400,
                detail="Only card payment methods are supported"
            )

        card = stripe_pm.card

        if not card:

            raise HTTPException(
                status_code=400,
                detail="Card information not found"
            )

        # -------------------------------------------------
        # Check user's existing payment methods
        # -------------------------------------------------

        user_has_methods = db.query(PaymentMethod).filter(
            PaymentMethod.user_id == user_id
        ).count()

        # First card automatically becomes default
        is_default = user_has_methods == 0

        # -------------------------------------------------
        # Save payment method
        # -------------------------------------------------

        payment_method = PaymentMethod(

            user_id=user_id,

            stripe_payment_method_id=stripe_pm.id,

            type=stripe_pm.type,

            card_brand=card.brand,

            card_last4=card.last4,

            card_exp_month=card.exp_month,

            card_exp_year=card.exp_year,

            is_default=is_default
        )

        db.add(payment_method)

        db.commit()

        db.refresh(payment_method)

        return payment_method

    except stripe.error.StripeError as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# GET USER PAYMENT METHODS
# =========================================================

@router.get(
    "",
    response_model=list[PaymentMethodResponse]
)
def get_payment_methods(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # TODO:
    # JWT se current user lena hai
    user_id = current_user.id

    methods = db.query(PaymentMethod).filter(
        PaymentMethod.user_id == user_id
    ).order_by(
        PaymentMethod.is_default.desc(),
        PaymentMethod.created_at.desc()
    ).all()

    return methods