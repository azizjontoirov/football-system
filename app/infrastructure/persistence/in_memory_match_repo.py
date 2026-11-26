from app.domain.entities.match import Match
from app.domain.ports.match_repository import MatchRepositoryPort


class InMemoryMatchRepository(MatchRepositoryPort):
    def __init__(self):
        self._matches: list[Match] = []
        self._next_id: int = 1

    def save(self, tournament_id: int, home_team_id: int, away_team_id: int) -> Match:
        match = Match(
            id=self._next_id,
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
        )
        self._matches.append(match)
        self._next_id += 1
        return match

    def get_by_id(self, match_id: int) -> Match | None:
        for m in self._matches:
            if m.id == match_id:
                return m
        return None

    def get_by_tournament(self, tournament_id: int) -> list[Match]:
        return [m for m in self._matches if m.tournament_id == tournament_id]

    def update(self, match: Match) -> Match:
        for idx, existing in enumerate(self._matches):
            if existing.id == match.id:
                self._matches[idx] = match
                return match
        raise LookupError(f"ID={match.id} bo'lgan uchrashuv topilmadi")