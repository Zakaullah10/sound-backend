from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.faqs import FAQ
from app.schemas.faqs import FAQCreate, FAQUpdate, FAQResponse

router = APIRouter(prefix="/faqs", tags=["FAQs"])

@router.post("/", response_model=FAQResponse)
def create_faq(payload: FAQCreate, db: Session = Depends(get_db)):
    faq = FAQ(**payload.dict())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq

@router.get("/", response_model=List[FAQResponse])
def list_faqs(db: Session = Depends(get_db)):
    return db.query(FAQ).order_by(FAQ.display_order).all()

@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq

@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(faq_id: int, payload: FAQUpdate, db: Session = Depends(get_db)):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    for key, value in payload.dict().items():
        setattr(faq, key, value)
    db.commit()
    db.refresh(faq)
    return faq

@router.delete("/{faq_id}")
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db.delete(faq)
    db.commit()
    return {"detail": "FAQ deleted"}