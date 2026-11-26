from app.domain.entities.team import Team
from app.domain.events.football_events import TeamRegisteredEvent
from app.domain.ports.event_bus import EventBusPort
from app.domain.ports.team_repository import TeamRepositoryPort


class TeamUseCase:
    def __init__(self, team_repo: TeamRepositoryPort, event_bus: EventBusPort | None = None):
        self.team_repo = team_repo
        self.event_bus = event_bus

    def register_team(self, name: str, city: str) -> Team:
        for team in self.team_repo.get_all():
            if team.name.lower() == name.lower():
                raise ValueError(f"'{name}' nomli jamoa allaqachon ro'yxatdan o'tgan")
        team = self.team_repo.save(name=name, city=city)

        if self.event_bus:
            self.event_bus.publish(
                TeamRegisteredEvent(team_id=team.id, team_name=team.name, city=team.city)
            )
        return team

    def get_team(self, team_id: int) -> Team:
        team = self.team_repo.get_by_id(team_id)
        if not team:
            raise LookupError(f"ID={team_id} bo'lgan jamoa topilmadi")
        return team

    def list_teams(self) -> list[Team]:
        return self.team_repo.get_all()

    def delete_team(self, team_id: int) -> None:
        deleted = self.team_repo.delete(team_id)
        if not deleted:
            raise LookupError(f"ID={team_id} bo'lgan jamoa topilmadi")