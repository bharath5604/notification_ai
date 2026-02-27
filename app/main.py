from fastapi import FastAPI
from app.routes.notification_routes import router as notify_router
from app.routes.metrics_routes import router as metrics_router
from app.routes.rules_routes import router as rules_router

app = FastAPI(
    title="Smart Notification Engine",
    description="Rule-based Notification Decision System with Deduplication, Fatigue Control, and Fail-safe",
    version="1.0.0"
)

# Include all routes
app.include_router(notify_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")
app.include_router(rules_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Smart Notification Engine Running 🚀",
        "docs": "/docs",
        "metrics": "/api/metrics",
        "rules": "/api/rules"
    }