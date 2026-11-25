from abc import ABC, abstractmethod
from app.domain.entities.match import Match


class MatchRepositoryPort(ABC):
    @abstractmethod
    def save(self, tournament_id: int, home_team_id: int, away_team_id: int) -> Match:
        pass

    @abstractmethod
    def get_by_id(self, match_id: int) -> Match | None:
        pass

    @abstractmethod
    def get_by_tournament(self, tournament_id: int) -> list[Match]:
        pass

    @abstractmethod
    def update(self, match: Match) -> Match:
        pass