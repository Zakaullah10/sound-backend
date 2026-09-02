from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class NotificationSettingBase(BaseModel):
    settings: Dict[str, Any]   # ye kuch bhi json data accept kar lega

class NotificationSettingCreate(NotificationSettingBase):
    pass

class NotificationSettingUpdate(NotificationSettingBase):
    pass

class NotificationSettingResponse(NotificationSettingBase):
    id: int
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True