from pydantic import BaseModel, Field


class TeamCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    city: str = Field(..., min_length=2, max_length=100)


class PlayerCreateSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    team_id: int = Field(..., gt=0)
    jersey_number: int = Field(..., ge=1, le=99)
    position: str = Field(..., min_length=2, max_length=50)


class TournamentCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    season: str = Field(..., min_length=4, max_length=20)


class MatchCreateSchema(BaseModel):
    tournament_id: int = Field(..., gt=0)
    home_team_id: int = Field(..., gt=0)
    away_team_id: int = Field(..., gt=0)


class MatchResultSchema(BaseModel):
    home_score: int = Field(..., ge=0)
    away_score: int = Field(..., ge=0)