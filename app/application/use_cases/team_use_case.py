from app.domain.entities.team import Team
from app.domain.ports.team_repository import TeamRepositoryPort


class TeamUseCase:
    def __init__(self, team_repo: TeamRepositoryPort):
        self.team_repo = team_repo

    def register_team(self, name: str, city: str) -> Team:
        existing_teams = self.team_repo.get_all()
        for team in existing_teams:
            if team.name.lower() == name.lower():
                raise ValueError(f"'{name}' nomli jamoa allaqachon ro'yxatdan o'tgan")
        return self.team_repo.save(name=name, city=city)

    def list_teams(self) -> list[Team]:
        return self.team_repo.get_all()