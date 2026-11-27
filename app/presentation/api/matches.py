from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.tournament_use_case import TournamentUseCase
from app.core.auth import require_roles
from app.core.dependencies import get_tournament_use_case
from app.domain.entities.user import User, UserRole
from app.presentation.api.schemas import (
    ErrorResponseSchema,
    MatchCreateSchema,
    MatchResponseSchema,
    MatchResultSchema,
)

router = APIRouter(prefix="/matches", tags=["Uchrashuvlar"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MatchResponseSchema,
    summary="Yangi uchrashuv belgilash",
    description="Turnir doirasida mezbon va mehmon jamoalar o'rtasida o'yin belgilaydi.",
    responses={
        400: {"model": ErrorResponseSchema, "description": "Jamoa o'ziga qarshi o'ynashi mumkin emas"},
        404: {"model": ErrorResponseSchema, "description": "Turnir yoki jamoa topilmadi"},
    },
)
def create_match(
    payload: MatchCreateSchema,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.ORGANIZER)),
):
    try:
        match = use_case.schedule_match(
            tournament_id=payload.tournament_id,
            home_team_id=payload.home_team_id,
            away_team_id=payload.away_team_id,
        )
        return asdict(match)
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.patch(
    "/{match_id}/result",
    response_model=MatchResponseSchema,
    summary="Uchrashuv hisobini kiritish",
    description="Belgilangan uchrashuvning yakuniy hisobini kiritadi va uning holatini `finished` ga o'zgartiradi.",
    responses={
        400: {"model": ErrorResponseSchema, "description": "Gollar soni manfiy bo'lishi mumkin emas"},
        404: {"model": ErrorResponseSchema, "description": "Uchrashuv topilmadi"},
    },
)
def update_match_result(
    match_id: int,
    payload: MatchResultSchema,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.ORGANIZER)),
):
    try:
        match = use_case.record_match_result(
            match_id=match_id,
            home_score=payload.home_score,
            away_score=payload.away_score,
        )
        return asdict(match)
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))