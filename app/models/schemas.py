from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationEvent(BaseModel):
    user_id: str
    event_type: Optional[str] = None
    message: str
    source: Optional[str] = None
    priority_hint: Optional[str] = None
    timestamp: Optional[datetime] = None
    channel: Optional[str] = None
    dedupe_key: Optional[str] = None
    expires_at: Optional[datetime] = None
