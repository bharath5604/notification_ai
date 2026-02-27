from fastapi import APIRouter
from app.services.metrics_service import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():
    """
    Returns system metrics for monitoring notification engine performance.
    """
    data = get_metrics()

    return {
        "status": "success",
        "metrics": data
    }