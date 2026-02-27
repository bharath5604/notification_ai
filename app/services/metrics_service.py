from app.database import audit_collection

# Default metrics template
DEFAULT_METRICS = {
    "sent": 0,
    "blocked": 0,
    "failed": 0,
    "queued": 0,
    "duplicates": 0,
    "fatigue_blocked": 0
}


def update_metric(key):
    """
    Increment metric counter in DB.
    """

    audit_collection.update_one(
        {"_id": "metrics"},
        {"$inc": {key: 1}},
        upsert=True
    )


def get_metrics():
    """
    Retrieve metrics from DB.
    """

    data = audit_collection.find_one({"_id": "metrics"})

    if not data:
        return DEFAULT_METRICS

    # Remove MongoDB internal id
    data.pop("_id", None)

    return data