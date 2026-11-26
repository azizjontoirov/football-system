from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.tournament_use_case import TournamentUseCase
from app.core.dependencies import get_tournament_use_case
from app.presentation.api.schemas import MatchCreateSchema, MatchResultSchema

router = APIRouter(prefix="/matches", tags=["Uchrashuvlar"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_match(
    payload: MatchCreateSchema,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
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


@router.patch("/{match_id}/result")
def update_match_result(
    match_id: int,
    payload: MatchResultSchema,
    use_case: TournamentUseCase = Depends(get_tournament_use_case),
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