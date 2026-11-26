from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.use_cases.tournament_use_case import TournamentUseCase
from app.core.dependencies import get_tournament_use_case
from app.presentation.api.schemas import (
    ErrorResponseSchema,
    MatchResponseSchema,
    StandingResponseSchema,
    TournamentCreateSchema,
    TournamentResponseSchema,
)

router = APIRouter(prefix="/tournaments", tags=["Turnirlar"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TournamentResponseSchema,
    summary="Yangi turnir yaratish",
    description="Yangi havaskor futbol musobaqasi va uning mavsumini ro'yxatdan o'tkazadi.",
)
def create_tournament(
    payload: TournamentCreateSchema,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
):
    return asdict(use_case.create_tournament(name=payload.name, season=payload.season))


@router.get(
    "/",
    response_model=list[TournamentResponseSchema],
    summary="Barcha turnirlar ro'yxatini olish",
)
def get_tournaments(use_case: TournamentUseCase = Depends(get_tournament_use_case)):
    return [asdict(t) for t in use_case.list_tournaments()]


@router.get(
    "/{tournament_id}/matches",
    response_model=list[MatchResponseSchema],
    summary="Turnir uchrashuvlari ro'yxatini olish",
    responses={404: {"model": ErrorResponseSchema, "description": "Turnir topilmadi"}},
)
def get_tournament_matches(
    tournament_id: int,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
):
    try:
        return [asdict(m) for m in use_case.list_matches(tournament_id)]
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get(
    "/{tournament_id}/standings",
    response_model=list[StandingResponseSchema],
    summary="Turnir jadvalini hisoblash va olish",
    description=(
        "Tugagan uchrashuvlar asosida tanlangan strategiya (`standard` yoki `bonus`) "
        "bo'yicha turnir jadvalini saralab qaytaradi."
    ),    responses={
        400: {"model": ErrorResponseSchema, "description": "Noma'lum scoring qoidasi"},
        404: {"model": ErrorResponseSchema, "description": "Turnir topilmadi"},
    },
)
def get_tournament_standings(
    tournament_id: int,
    scoring: str = Query(
        "standard",
        description="Hisoblash qoidasi: `standard` (3-1-0) yoki `bonus` (3+ golga +1 ochko)",
    ),    use_case: TournamentUseCase = Depends(get_tournament_use_case),
):
    try:
        standings = use_case.get_standings(tournament_id=tournament_id, scoring_rule=scoring)
        return [
            {**asdict(row), "goal_difference": row.goal_difference}
            for row in standings
        ]
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))