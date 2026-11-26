from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.application.use_cases.player_use_case import PlayerUseCase
from app.application.use_cases.team_use_case import TeamUseCase
from app.core.dependencies import get_player_use_case, get_team_use_case
from app.presentation.api.schemas import TeamCreateSchema

router = APIRouter(prefix="/teams", tags=["Jamoalar"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_team(
    payload: TeamCreateSchema,
    use_case: TeamUseCase = Depends(get_team_use_case),
):
    try:
        return asdict(use_case.register_team(name=payload.name, city=payload.city))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/")
def get_teams(use_case: TeamUseCase = Depends(get_team_use_case)):
    return [asdict(team) for team in use_case.list_teams()]


@router.get("/{team_id}")
def get_team_by_id(team_id: int, use_case: TeamUseCase = Depends(get_team_use_case)):
    try:
        return asdict(use_case.get_team(team_id))
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, use_case: TeamUseCase = Depends(get_team_use_case)):
    try:
        use_case.delete_team(team_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/{team_id}/players")
def get_team_players(
    team_id: int,
    use_case: PlayerUseCase = Depends(get_player_use_case),
):
    try:
        return [asdict(p) for p in use_case.list_by_team(team_id)]
    except LookupError as err:
        raise HTTPException(status_code=404, detail=str(err))