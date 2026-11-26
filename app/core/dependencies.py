from functools import lru_cache
from fastapi import Depends

from app.application.use_cases.team_use_case import TeamUseCase
from app.domain.ports.team_repository import TeamRepositoryPort
from app.infrastructure.persistence.in_memory_team_repo import InMemoryTeamRepository


@lru_cache(maxsize=1)
def get_team_repository() -> TeamRepositoryPort:
    """Singleton: butun ilova bo'yicha yagona ombor nusxasini qaytaradi."""
    return InMemoryTeamRepository()


def get_team_use_case(
    repo: TeamRepositoryPort = Depends(get_team_repository),
) -> TeamUseCase:
    """Dependency Injection: UseCase ga omborni tashqaridan kiritib beradi."""
    return TeamUseCase(team_repo=repo)
