from abc import ABC, abstractmethod

from app.domain.entities.tournament import Tournament


class TournamentRepositoryPort(ABC):
    @abstractmethod
    def save(self, name: str, season: str) -> Tournament:
        pass

    @abstractmethod
    def get_by_id(self, tournament_id: int) -> Tournament | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Tournament]:
        pass