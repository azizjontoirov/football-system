from functools import lru_cache
from fastapi import Depends

from app.application.use_cases.player_use_case import PlayerUseCase
from app.application.use_cases.team_use_case import TeamUseCase
from app.application.use_cases.tournament_use_case import TournamentUseCase
from app.domain.ports.match_repository import MatchRepositoryPort
from app.domain.ports.player_repository import PlayerRepositoryPort
from app.domain.ports.team_repository import TeamRepositoryPort
from app.domain.ports.tournament_repository import TournamentRepositoryPort
from app.infrastructure.persistence.in_memory_match_repo import InMemoryMatchRepository
from app.infrastructure.persistence.in_memory_player_repo import InMemoryPlayerRepository
from app.infrastructure.persistence.in_memory_team_repo import InMemoryTeamRepository
from app.infrastructure.persistence.in_memory_tournament_repo import InMemoryTournamentRepository


@lru_cache(maxsize=1)
def get_team_repository() -> TeamRepositoryPort:
    return InMemoryTeamRepository()


@lru_cache(maxsize=1)
def get_player_repository() -> PlayerRepositoryPort:
    return InMemoryPlayerRepository()


@lru_cache(maxsize=1)
def get_tournament_repository() -> TournamentRepositoryPort:
    return InMemoryTournamentRepository()


@lru_cache(maxsize=1)
def get_match_repository() -> MatchRepositoryPort:
    return InMemoryMatchRepository()


def get_team_use_case(
    repo: TeamRepositoryPort = Depends(get_team_repository),
) -> TeamUseCase:
    return TeamUseCase(team_repo=repo)


def get_player_use_case(
    player_repo: PlayerRepositoryPort = Depends(get_player_repository),
    team_repo: TeamRepositoryPort = Depends(get_team_repository),
) -> PlayerUseCase:
    return PlayerUseCase(player_repo=player_repo, team_repo=team_repo)


def get_tournament_use_case(
    tournament_repo: TournamentRepositoryPort = Depends(get_tournament_repository),
    match_repo: MatchRepositoryPort = Depends(get_match_repository),
    team_repo: TeamRepositoryPort = Depends(get_team_repository),
) -> TournamentUseCase:
    return TournamentUseCase(
        tournament_repo=tournament_repo,
        match_repo=match_repo,
        team_repo=team_repo,
    )