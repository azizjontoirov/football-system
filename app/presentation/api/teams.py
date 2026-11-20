from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.use_cases.team_use_case import TeamUseCase
from app.infrastructure.persistence.in_memory_team_repo import InMemoryTeamRepository

router = APIRouter(prefix="/teams", tags=["Jamoalar"])

# Adapter va Use Case ni bog'lash (5-laboratoriyada DI container orqali boshqariladi)
_repo = InMemoryTeamRepository()
_use_case = TeamUseCase(team_repo=_repo)


class TeamCreateSchema(BaseModel):
    name: str
    city: str


@router.post("/", status_code=201)
def create_team(payload: TeamCreateSchema):
    try:
        team = _use_case.register_team(name=payload.name, city=payload.city)
        return asdict(team)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))


@router.get("/")
def get_teams():
    teams = _use_case.list_teams()
    return [asdict(team) for team in teams]