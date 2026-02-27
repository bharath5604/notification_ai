from fastapi import APIRouter
from app.models.schemas import NotificationEvent
from app.services.decision_engine import decide
from app.database import events_collection
from datetime import datetime

router = APIRouter()


@router.post("/notify")
def notify(request: NotificationEvent):

    # ⭐ Log incoming event
    events_collection.insert_one({
        "event": request.dict(),
        "received_at": datetime.utcnow()
    })

    return decide(request)