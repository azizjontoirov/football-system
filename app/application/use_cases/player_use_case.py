from app.domain.entities.player import Player
from app.domain.ports.player_repository import PlayerRepositoryPort
from app.domain.ports.team_repository import TeamRepositoryPort


class PlayerUseCase:
    def __init__(self, player_repo: PlayerRepositoryPort, team_repo: TeamRepositoryPort):
        self.player_repo = player_repo
        self.team_repo = team_repo

    def register_player(
        self, full_name: str, team_id: int, jersey_number: int, position: str
    ) -> Player:
        if not self.team_repo.get_by_id(team_id):
            raise LookupError(f"ID={team_id} bo'lgan jamoa topilmadi")

        for existing in self.player_repo.get_by_team(team_id):
            if existing.jersey_number == jersey_number:
                raise ValueError(f"Bu jamoada #{jersey_number} raqami allaqachon band")

        return self.player_repo.save(
            full_name=full_name,
            team_id=team_id,
            jersey_number=jersey_number,
            position=position,
        )

    def list_by_team(self, team_id: int) -> list[Player]:
        if not self.team_repo.get_by_id(team_id):
            raise LookupError(f"ID={team_id} bo'lgan jamoa topilmadi")
        return self.player_repo.get_by_team(team_id)