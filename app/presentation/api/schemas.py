from pydantic import BaseModel, ConfigDict, Field


class ErrorResponseSchema(BaseModel):
    detail: str = Field(..., description="Xatolik haqida qisqacha izoh")

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "ID=99 bo'lgan jamoa topilmadi"}}
    )


class TeamCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Jamoaning rasmiy nomi")
    city: str = Field(..., min_length=2, max_length=100, description="Jamoa joylashgan shahar yoki tuman")

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Samarqand United", "city": "Samarqand"}}
    )


class TeamResponseSchema(BaseModel):
    id: int = Field(..., description="Jamoaning unikal identifikatori")
    name: str = Field(..., description="Jamoa nomi")
    city: str = Field(..., description="Shahar nomi")

    model_config = ConfigDict(
        json_schema_extra={"example": {"id": 1, "name": "Samarqand United", "city": "Samarqand"}}
    )


class PlayerCreateSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, description="O'yinchining ism-familiyasi")
    team_id: int = Field(..., gt=0, description="O'yinchi biriktiriladigan jamoa ID raqami")
    jersey_number: int = Field(..., ge=1, le=99, description="Futbolka raqami (1–99 oralig'ida)")
    position: str = Field(..., min_length=2, max_length=50, description="Maydondagi pozitsiyasi")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Azizbek Karimov",
                "team_id": 1,
                "jersey_number": 10,
                "position": "Hujumchi",
            }
        }
    )


class PlayerResponseSchema(BaseModel):
    id: int
    full_name: str
    team_id: int
    jersey_number: int
    position: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "full_name": "Azizbek Karimov",
                "team_id": 1,
                "jersey_number": 10,
                "position": "Hujumchi",
            }
        }
    )


class TournamentCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=150, description="Turnir nomi")
    season: str = Field(..., min_length=4, max_length=20, description="Musobaqa mavsumi")

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Samarqand Havaskorlar Kubogi", "season": "2026"}}
    )


class TournamentResponseSchema(BaseModel):
    id: int
    name: str
    season: str
    status: str = Field(..., description="Turnir holati: upcoming, active yoki finished")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Samarqand Havaskorlar Kubogi",
                "season": "2026",
                "status": "upcoming",
            }
        }
    )


class MatchCreateSchema(BaseModel):
    tournament_id: int = Field(..., gt=0, description="Turnir ID raqami")
    home_team_id: int = Field(..., gt=0, description="Mezbon jamoa ID raqami")
    away_team_id: int = Field(..., gt=0, description="Mehmon jamoa ID raqami")

    model_config = ConfigDict(
        json_schema_extra={"example": {"tournament_id": 1, "home_team_id": 1, "away_team_id": 2}}
    )


class MatchResultSchema(BaseModel):
    home_score: int = Field(..., ge=0, description="Mezbon jamoa urgan gollar soni")
    away_score: int = Field(..., ge=0, description="Mehmon jamoa urgan gollar soni")

    model_config = ConfigDict(
        json_schema_extra={"example": {"home_score": 3, "away_score": 1}}
    )


class MatchResponseSchema(BaseModel):
    id: int
    tournament_id: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    status: str = Field(..., description="Uchrashuv holati: scheduled yoki finished")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "tournament_id": 1,
                "home_team_id": 1,
                "away_team_id": 2,
                "home_score": 3,
                "away_score": 1,
                "status": "finished",
            }
        }
    )


class StandingResponseSchema(BaseModel):
    team_id: int
    team_name: str
    played: int = Field(..., description="O'tkazilgan o'yinlar soni")
    won: int = Field(..., description="G'alabalar soni")
    drawn: int = Field(..., description="Duranglar soni")
    lost: int = Field(..., description="Mag'lubiyatlar soni")
    goals_for: int = Field(..., description="Urilgan gollar")
    goals_against: int = Field(..., description="O'tkazib yuborilgan gollar")
    goal_difference: int = Field(..., description="To'plar nisbati")
    points: int = Field(..., description="To'plangan ochkolar")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "team_id": 1,
                "team_name": "Samarqand United",
                "played": 1,
                "won": 1,
                "drawn": 0,
                "lost": 0,
                "goals_for": 3,
                "goals_against": 1,
                "goal_difference": 2,
                "points": 3,
            }
        }
    )