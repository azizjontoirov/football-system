from app.domain.entities.team import Team
from app.domain.ports.team_repository import TeamRepositoryPort


class InMemoryTeamRepository(TeamRepositoryPort):
    """Ma'lumotlarni vaqtinchalik xotirada saqlovchi adapter."""

    def __init__(self):
        self._teams: list[Team] = []
        self._next_id: int = 1

    def save(self, name: str, city: str) -> Team:
        team = Team(id=self._next_id, name=name, city=city)
        self._teams.append(team)
        self._next_id += 1
        return team

    def get_all(self) -> list[Team]:
        return list(self._teams)