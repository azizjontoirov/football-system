from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.event_handlers.notification_handlers import NotificationFeedHandler
from app.application.use_cases.player_use_case import PlayerUseCase
from app.application.use_cases.team_use_case import TeamUseCase
from app.application.use_cases.tournament_use_case import TournamentUseCase
from app.domain.events.football_events import MatchFinishedEvent, TeamRegisteredEvent
from app.domain.ports.event_bus import EventBusPort
from app.domain.ports.match_repository import MatchRepositoryPort
from app.domain.ports.player_repository import PlayerRepositoryPort
from app.domain.ports.team_repository import TeamRepositoryPort
from app.domain.ports.tournament_repository import TournamentRepositoryPort
from app.infrastructure.database.session import get_db
from app.infrastructure.messaging.in_memory_event_bus import InMemoryEventBus
from app.infrastructure.persistence.sqlalchemy_repos import (
    SQLAlchemyMatchRepository,
    SQLAlchemyPlayerRepository,
    SQLAlchemyTeamRepository,
    SQLAlchemyTournamentRepository,
)


@lru_cache(maxsize=1)
def get_notification_store() -> list[dict]:
    """Hodisalar asosida shakllangan bildirishnomalar lentasi (Singleton)."""
    return []


@lru_cache(maxsize=1)
def get_event_bus() -> EventBusPort:
    """Yagona EventBus nusxasini yaratib, obunachilarni ulaydi."""
    bus = InMemoryEventBus()
    handler = NotificationFeedHandler(store=get_notification_store())
    bus.subscribe(TeamRegisteredEvent, handler.on_team_registered)
    bus.subscribe(MatchFinishedEvent, handler.on_match_finished)
    return bus


def get_team_repository(db: Session = Depends(get_db)) -> TeamRepositoryPort:
    return SQLAlchemyTeamRepository(db)


def get_player_repository(db: Session = Depends(get_db)) -> PlayerRepositoryPort:
    return SQLAlchemyPlayerRepository(db)


def get_tournament_repository(db: Session = Depends(get_db)) -> TournamentRepositoryPort:
    return SQLAlchemyTournamentRepository(db)


def get_match_repository(db: Session = Depends(get_db)) -> MatchRepositoryPort:
    return SQLAlchemyMatchRepository(db)


def get_team_use_case(
    repo: TeamRepositoryPort = Depends(get_team_repository),
    event_bus: EventBusPort = Depends(get_event_bus),
) -> TeamUseCase:
    return TeamUseCase(team_repo=repo, event_bus=event_bus)


def get_player_use_case(
    player_repo: PlayerRepositoryPort = Depends(get_player_repository),
    team_repo: TeamRepositoryPort = Depends(get_team_repository),
) -> PlayerUseCase:
    return PlayerUseCase(player_repo=player_repo, team_repo=team_repo)


def get_tournament_use_case(
    tournament_repo: TournamentRepositoryPort = Depends(get_tournament_repository),
    match_repo: MatchRepositoryPort = Depends(get_match_repository),
    team_repo: TeamRepositoryPort = Depends(get_team_repository),
    event_bus: EventBusPort = Depends(get_event_bus),
) -> TournamentUseCase:
    return TournamentUseCase(
        tournament_repo=tournament_repo,
        match_repo=match_repo,
        team_repo=team_repo,
        event_bus=event_bus,
    )