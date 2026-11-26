from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.application.use_cases.player_use_case import PlayerUseCase
from app.application.use_cases.team_use_case import TeamUseCase
from app.core.dependencies import get_player_use_case, get_team_use_case
from app.presentation.api.schemas import (
    ErrorResponseSchema,
    PlayerResponseSchema,
    TeamCreateSchema,
    TeamResponseSchema,
)

router = APIRouter(prefix="/teams", tags=["Jamoalar"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamResponseSchema,
    summary="Yangi jamoani ro'yxatdan o'tkazish",
    description="Tizimga yangi havaskor futbol jamoasini qo'shadi. Bir xil nomdagi jamoani qayta qo'shish taqiqlanadi.",
    responses={400: {"model": ErrorResponseSchema, "description": "Jamoa nomi band yoki noto'g'ri"}},
)
def create_team(
    payload: TeamCreateSchema,
    use_case: TeamUseCase = Depends(get_team_use_case),
):
    try:
        return asdict(use_case.register_team(name=payload.name, city=payload.city))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get(
    "/",
    response_model=list[TeamResponseSchema],
    summary="Barcha jamoalar ro'yxatini olish",
    description="Tizimda ro'yxatdan o'tgan barcha futbol jamoalarini qaytaradi.",
)
def get_teams(use_case: TeamUseCase = Depends(get_team_use_case)):
    return [asdict(team) for team in use_case.list_teams()]


@router.get(
    "/{team_id}",
    response_model=TeamResponseSchema,
    summary="Jamoani ID bo'yicha olish",
    responses={404: {"model": ErrorResponseSchema, "description": "Jamoa topilmadi"}},
)
def get_team_by_id(team_id: int, use_case: TeamUseCase = Depends(get_team_use_case)):
    try:
        return asdict(use_case.get_team(team_id))
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Jamoani o'chirish",
    responses={404: {"model": ErrorResponseSchema, "description": "Jamoa topilmadi"}},
)
def delete_team(team_id: int, use_case: TeamUseCase = Depends(get_team_use_case)):
    try:
        use_case.delete_team(team_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get(
    "/{team_id}/players",
    response_model=list[PlayerResponseSchema],
    summary="Jamoa o'yinchilari ro'yxatini olish",
    responses={404: {"model": ErrorResponseSchema, "description": "Jamoa topilmadi"}},
)
def get_team_players(
    team_id: int,
    use_case: PlayerUseCase = Depends(get_player_use_case),
):
    try:
        return [asdict(p) for p in use_case.list_by_team(team_id)]
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))