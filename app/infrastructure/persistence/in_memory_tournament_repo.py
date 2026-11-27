from app.domain.entities.tournament import Tournament
from app.domain.ports.tournament_repository import TournamentRepositoryPort


class InMemoryTournamentRepository(TournamentRepositoryPort):
    def __init__(self):
        self._tournaments: list[Tournament] = []
        self._next_id: int = 1

    def save(self, name: str, season: str) -> Tournament:
        tournament = Tournament(id=self._next_id, name=name, season=season)
        self._tournaments.append(tournament)
        self._next_id += 1
        return tournament

    def get_by_id(self, tournament_id: int) -> Tournament | None:
        for t in self._tournaments:
            if t.id == tournament_id:
                return t
        return None

    def get_all(self) -> list[Tournament]:
        return list(self._tournaments)