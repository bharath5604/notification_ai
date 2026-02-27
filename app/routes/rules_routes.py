from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

router = APIRouter()

# ✅ Make path absolute for reliability
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RULES_FILE = os.path.join(BASE_DIR, "app","config", "rules.json")


# 📦 Request model for updating rules
class RulesUpdate(BaseModel):
    business_hours: dict | None = None
    allowed_channels: list[str] | None = None
    fatigue: dict | None = None   # Nested fatigue update


# 🔹 GET CURRENT RULES
@router.get("/rules")
def get_rules():
    """
    Returns current system rules directly from JSON.
    """
    with open(RULES_FILE, "r") as f:
        rules = json.load(f)

    return {
        "status": "success",
        "rules": rules
    }


# 🔹 UPDATE RULES
@router.post("/rules")
def update_rules(new_rules: RulesUpdate):
    """
    Updates configurable rules dynamically.
    """
    # Load current rules from file
    with open(RULES_FILE, "r") as f:
        rules = json.load(f)

    # Update only provided fields
    if new_rules.business_hours:
        rules["business_hours"] = new_rules.business_hours

    if new_rules.allowed_channels:
        rules["allowed_channels"] = new_rules.allowed_channels

    if new_rules.fatigue:
        rules["fatigue"] = new_rules.fatigue

    # Save updated rules back to file
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=4)

    return {
        "status": "updated",
        "rules": rules
    }