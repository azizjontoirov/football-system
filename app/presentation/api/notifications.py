from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.dependencies import get_notification_store

router = APIRouter(prefix="/notifications", tags=["Hodisalar va bildirishnomalar"])


class NotificationResponseSchema(BaseModel):
    event_type: str
    message: str
    occurred_at: str


@router.get(
    "/",
    response_model=list[NotificationResponseSchema],
    summary="Tizim hodisalari va bildirishnomalar lentasini olish",
    description=(
        "EventBus orqali qayta ishlangan so'nggi domen hodisalari "
        "(yangi jamoalar, tugagan o'yinlar) ro'yxatini qaytaradi."
    ),)
def get_notifications(store: list[dict] = Depends(get_notification_store)):
    return list(reversed(store))
