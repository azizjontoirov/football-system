from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.player_use_case import PlayerUseCase
from app.core.dependencies import get_player_use_case
from app.presentation.api.schemas import (
    ErrorResponseSchema,
    PlayerCreateSchema,
    PlayerResponseSchema,
)

router = APIRouter(prefix="/players", tags=["O'yinchilar"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PlayerResponseSchema,
    summary="Jamoaga yangi o'yinchi qo'shish",
    description="Tanlangan jamoaga yangi futbolchini biriktiradi. Bitta jamoada bir xil futbolka raqami takrorlanmasligi tekshiriladi.",
    responses={
        400: {"model": ErrorResponseSchema, "description": "Futbolka raqami band yoki noto'g'ri"},
        404: {"model": ErrorResponseSchema, "description": "Ko'rsatilgan jamoa topilmadi"},
    },
)
def create_player(
    payload: PlayerCreateSchema,
    use_case: PlayerUseCase = Depends(get_player_use_case),
):
    try:
        player = use_case.register_player(
            full_name=payload.full_name,
            team_id=payload.team_id,
            jersey_number=payload.jersey_number,
            position=payload.position,
        )
        return asdict(player)
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))