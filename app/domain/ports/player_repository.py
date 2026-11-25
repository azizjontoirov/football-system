from abc import ABC, abstractmethod
from app.domain.entities.player import Player


class PlayerRepositoryPort(ABC):
    @abstractmethod
    def save(self, full_name: str, team_id: int, jersey_number: int, position: str) -> Player:
        pass

    @abstractmethod
    def get_by_team(self, team_id: int) -> list[Player]:
        pass