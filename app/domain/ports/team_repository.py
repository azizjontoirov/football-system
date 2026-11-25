from abc import ABC, abstractmethod
from app.domain.entities.team import Team


class TeamRepositoryPort(ABC):
    @abstractmethod
    def save(self, name: str, city: str) -> Team:
        pass

    @abstractmethod
    def get_by_id(self, team_id: int) -> Team | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Team]:
        pass