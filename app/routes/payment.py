from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.payment import CheckoutSessionCreate, CheckoutSessionResponse
from app.services.stripe_service import create_checkout_session
from app.services.webhook_service import handle_stripe_webhook
from app.dependencies.auth import get_current_user   # aapka existing auth dependency
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/checkout", response_model=CheckoutSessionResponse)
def checkout(
    data: CheckoutSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        url = create_checkout_session(db, current_user, data.plan_id)
        return {"checkout_url": url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        result = handle_stripe_webhook(payload, sig_header, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))