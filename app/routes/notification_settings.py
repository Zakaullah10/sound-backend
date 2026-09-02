from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.notification_settings import NotificationSettingCreate, NotificationSettingResponse
from app.models.notification_settings import NotificationSetting
from app.dependencies.auth import get_current_user  # apka existing auth dependency

router = APIRouter(prefix="/notification-settings", tags=["Notification Settings"])

@router.get("/", response_model=NotificationSettingResponse)
def get_settings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    setting = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == current_user.id
    ).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Settings not found")
    return setting

@router.post("/", response_model=NotificationSettingResponse)
def create_or_update_settings(
    payload: NotificationSettingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    setting = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == current_user.id
    ).first()

    if setting:
        # Already hai to update kar do
        setting.settings = payload.settings
    else:
        # Nahi hai to naya bana do
        setting = NotificationSetting(
            user_id=current_user.id,
            settings=payload.settings
        )
        db.add(setting)

    db.commit()
    db.refresh(setting)
    return setting