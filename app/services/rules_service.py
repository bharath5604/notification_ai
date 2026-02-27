from datetime import datetime
import json
import os
from app.config import RULES


# ⭐ Return full rules (needed by fatigue service)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.json")

def get_rules():
    with open(RULES_PATH, "r") as f:
        return json.load(f)


# ⭐ Business Hours Check
def is_business_hours(timestamp=None):
    """
    Checks whether a given timestamp falls within business hours.
    If no timestamp provided, uses current UTC time.
    """

    if timestamp:
        now_hour = timestamp.hour
    else:
        now_hour = datetime.utcnow().hour

    start = RULES["business_hours"]["start"]
    end = RULES["business_hours"]["end"]

    return start <= now_hour < end


# ⭐ Channel Validation
def is_channel_allowed(channel):
    """
    Checks if the notification channel is allowed.
    """
    if not channel:
        return True

    return channel in RULES["allowed_channels"]


# ⭐ Fatigue Rules Access
def get_fatigue_rules():
    """
    Returns fatigue configuration from rules.json
    """
    return RULES.get("fatigue", {})