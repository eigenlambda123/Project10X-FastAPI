from fastapi import APIRouter, Depends, Request
import datetime

router = APIRouter()

start_time = datetime.datetime.utcnow()

@router.get("/metrics", tags=["Observability"])
def get_metrics():
    """
    GET Metrics endpoint to monitor application health and uptime
    """
    uptime = datetime.datetime.utcnow() - start_time
    return {
        "status": "ok",
        "uptime_seconds": int(uptime.total_seconds()),
        "message": "Metrics endpoint active"
    }
