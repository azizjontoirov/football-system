import json

from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.core.config import settings
from app.core.logging_config import LOG_FILE
from app.core.metrics import metrics_collector
from app.domain.entities.user import User, UserRole
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/monitoring", tags=["Monitoring va metrikalar"])


@router.get(
    "/health/detailed",
    summary="Tizim va ma'lumotlar bazasi holatini chuqur tekshirish",
)
def detailed_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    summary = metrics_collector.get_summary()
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
        "uptime_seconds": summary["uptime_seconds"],
        "total_requests": summary["total_requests"],
    }


@router.get(
    "/metrics",
    summary="Tizim ko'rsatkichlarini JSON formatida olish",
)
def get_metrics():
    return metrics_collector.get_summary()


@router.get(
    "/metrics/prometheus",
    response_class=PlainTextResponse,
    summary="Tizim ko'rsatkichlarini Prometheus formatida olish",
)
def get_prometheus_metrics():
    return metrics_collector.to_prometheus()


@router.get(
    "/logs",
    summary="So'nggi strukturalangan jurnallarni olish (faqat Admin)",
)
def get_recent_logs(
    limit: int = Query(20, ge=1, le=100, description="Qaytariladigan so'nggi log yozuvlari soni"),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    if not LOG_FILE.exists():
        return {"count": 0, "logs": []}

    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    recent = []
    for line in lines[-limit:]:
        try:
            recent.append(json.loads(line))
        except json.JSONDecodeError:
            recent.append({"raw": line})
    return {"count": len(recent), "logs": recent}