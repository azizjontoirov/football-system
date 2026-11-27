from dataclasses import dataclass, field
from datetime import datetime, timezone


class DomainEvent:
    """Barcha domen hodisalari uchun bazaviy klass."""
    pass


@dataclass(frozen=True)
class TeamRegisteredEvent(DomainEvent):
    team_id: int
    team_name: str
    city: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class MatchFinishedEvent(DomainEvent):
    tournament_id: int
    match_id: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))