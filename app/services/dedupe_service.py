from difflib import SequenceMatcher
from datetime import datetime, timedelta
from app.database import notification_log_collection

# Threshold for near-duplicate similarity
SIMILARITY_THRESHOLD = 0.85

# Time window to check duplicates (e.g., last 60 minutes)
DUPLICATE_WINDOW_MINUTES = 60


def is_duplicate(new_message, user_id):
    """
    Checks if a similar notification was sent recently for the SAME user.
    """
    time_limit = datetime.utcnow() - timedelta(minutes=DUPLICATE_WINDOW_MINUTES)

    recent_notifications = notification_log_collection.find(
        {"timestamp": {"$gte": time_limit}, "user_id": user_id}
    )

    for notif in recent_notifications:
        similarity = SequenceMatcher(None, new_message, notif["message"]).ratio()
        if similarity > SIMILARITY_THRESHOLD:
            return True

    return False


def log_notification(message):
    """
    Save notification to DB after sending.
    Required for future duplicate checks.
    """

    notification_log_collection.insert_one({
        "message": message,
        "timestamp": datetime.utcnow()
    })