from datetime import datetime

from app.services.rules_service import is_business_hours, is_channel_allowed
from app.services.dedupe_service import is_duplicate, log_notification
from app.services.fatigue_service import is_fatigued, update_user_history
from app.services.metrics_service import update_metric
from app.services.fail_safe_service import safe_run

from app.database import queue_collection


def decide(notification):
    """
    Main decision engine for notification prioritization.
    Returns NOW / LATER / NEVER with reason.
    Wrapped in fail-safe mode.
    """

    def core_logic():

        # 🕒 Ensure timestamp exists
        timestamp = notification.timestamp or datetime.utcnow()

        # 1️⃣ Business hours rule
        if not is_business_hours():
            update_metric("blocked")
            update_metric("queued")

            queue_collection.insert_one({
                "notification": notification.dict(),
                "reason": "Outside business hours",
                "created_at": datetime.utcnow()
            })

            return {
                "decision": "LATER",
                "reason": "Outside business hours"
            }

        # 2️⃣ Channel validation
        if notification.channel and not is_channel_allowed(notification.channel):
            update_metric("blocked")
            return {
                "decision": "NEVER",
                "reason": "Channel not allowed"
            }

        # 3️⃣ Expiry check
        if notification.expires_at and notification.expires_at < timestamp:
            update_metric("blocked")
            return {
                "decision": "NEVER",
                "reason": "Notification expired"
            }

        # 4️⃣ Duplicate detection
        if is_duplicate(notification.message, notification.user_id):
            update_metric("duplicates")
            return {
                "decision": "NEVER",
                "reason": "Duplicate or near-duplicate notification"
            }

        # 5️⃣ Fatigue protection
        if is_fatigued(notification.user_id):
            update_metric("fatigue_blocked")
            update_metric("queued")

            queue_collection.insert_one({
                "notification": notification.dict(),
                "reason": "User fatigue protection",
                "created_at": datetime.utcnow()
            })

            return {
                "decision": "LATER",
                "reason": "User fatigue protection"
            }

        # 6️⃣ Priority handling
        if notification.priority_hint == "high":
            update_user_history(notification.user_id)
            log_notification(notification.message)
            update_metric("sent")

            return {
                "decision": "NOW",
                "reason": "High priority notification"
            }

        if notification.priority_hint == "low":
            update_metric("blocked")
            update_metric("queued")

            queue_collection.insert_one({
                "notification": notification.dict(),
                "reason": "Low priority deferred",
                "created_at": datetime.utcnow()
            })

            return {
                "decision": "LATER",
                "reason": "Low priority deferred"
            }

        # 7️⃣ Default decision
        update_user_history(notification.user_id)
        log_notification(notification.message)
        update_metric("sent")

        return {
            "decision": "NOW",
            "reason": "Valid notification"
        }

    # 🔥 Fail-safe wrapper
    return safe_run(core_logic)