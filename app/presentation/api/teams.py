from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.use_cases.team_use_case import TeamUseCase
from app.core.dependencies import get_team_use_case

router = APIRouter(prefix="/teams", tags=["Jamoalar"])


class TeamCreateSchema(BaseModel):
    name: str
    city: str


@router.post("/", status_code=201)
def create_team(
    payload: TeamCreateSchema,
    use_case: TeamUseCase = Depends(get_team_use_case),
):
    try:
        team = use_case.register_team(name=payload.name, city=payload.city)
        return asdict(team)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/")
def get_teams(use_case: TeamUseCase = Depends(get_team_use_case)):
    teams = use_case.list_teams()
    return [asdict(team) for team in teams]