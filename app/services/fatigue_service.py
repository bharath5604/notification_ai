from app.database import history_collection
from datetime import datetime, timedelta
from app.services.rules_service import get_rules

def is_fatigued(user_id):
    """
    Checks whether user is in alert fatigue state.
    Uses configurable rules.
    """

    rules = get_rules()

    MAX_NOTIFICATIONS = rules["fatigue"]["max_notifications"]
    COOLDOWN_MINUTES = rules["fatigue"]["cooldown_minutes"]

    history = history_collection.find_one({"user_id": user_id})

    if not history:
        return False

    count = history.get("notifications_sent", 0)
    last_sent = history.get("last_sent_at")

    # If cooldown passed → reset fatigue
    if last_sent:
        if datetime.utcnow() - last_sent > timedelta(minutes=COOLDOWN_MINUTES):
            return False

    # Too many notifications
    if count >= MAX_NOTIFICATIONS:
        return True

    # Cooldown check
    if last_sent:
        if datetime.utcnow() - last_sent < timedelta(minutes=COOLDOWN_MINUTES):
            return True

    return False


def update_user_history(user_id):
    """
    Updates user notification history after sending.
    """

    history = history_collection.find_one({"user_id": user_id})

    if history:
        history_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {"notifications_sent": 1},
                "$set": {"last_sent_at": datetime.utcnow()}
            }
        )
    else:
        history_collection.insert_one({
            "user_id": user_id,
            "notifications_sent": 1,
            "last_sent_at": datetime.utcnow()
        })