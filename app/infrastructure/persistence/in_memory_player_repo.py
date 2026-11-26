from app.domain.entities.player import Player
from app.domain.ports.player_repository import PlayerRepositoryPort


class InMemoryPlayerRepository(PlayerRepositoryPort):
    def __init__(self):
        self._players: list[Player] = []
        self._next_id: int = 1

    def save(self, full_name: str, team_id: int, jersey_number: int, position: str) -> Player:
        player = Player(
            id=self._next_id,
            full_name=full_name,
            team_id=team_id,
            jersey_number=jersey_number,
            position=position,
        )
        self._players.append(player)
        self._next_id += 1
        return player

    def get_by_team(self, team_id: int) -> list[Player]:
        return [p for p in self._players if p.team_id == team_id]