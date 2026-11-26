from app.domain.entities.match import Match
from app.domain.entities.tournament import Tournament
from app.domain.events.football_events import MatchFinishedEvent
from app.domain.ports.event_bus import EventBusPort
from app.domain.ports.match_repository import MatchRepositoryPort
from app.domain.ports.team_repository import TeamRepositoryPort
from app.domain.ports.tournament_repository import TournamentRepositoryPort
from app.domain.services.standings_service import StandingsService, TeamStanding
from app.domain.strategies.scoring_strategy import ScoringStrategyFactory


class TournamentUseCase:
    def __init__(
        self,
        tournament_repo: TournamentRepositoryPort,
        match_repo: MatchRepositoryPort,
        team_repo: TeamRepositoryPort,
        event_bus: EventBusPort | None = None,
    ):
        self.tournament_repo = tournament_repo
        self.match_repo = match_repo
        self.team_repo = team_repo
        self.event_bus = event_bus

    def create_tournament(self, name: str, season: str) -> Tournament:
        return self.tournament_repo.save(name=name, season=season)

    def list_tournaments(self) -> list[Tournament]:
        return self.tournament_repo.get_all()

    def schedule_match(self, tournament_id: int, home_team_id: int, away_team_id: int) -> Match:
        if not self.tournament_repo.get_by_id(tournament_id):
            raise LookupError(f"ID={tournament_id} bo'lgan turnir topilmadi")
        if not self.team_repo.get_by_id(home_team_id):
            raise LookupError(f"Mezbon jamoa (ID={home_team_id}) topilmadi")
        if not self.team_repo.get_by_id(away_team_id):
            raise LookupError(f"Mehmon jamoa (ID={away_team_id}) topilmadi")

        return self.match_repo.save(
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
        )

    def list_matches(self, tournament_id: int) -> list[Match]:
        if not self.tournament_repo.get_by_id(tournament_id):
            raise LookupError(f"ID={tournament_id} bo'lgan turnir topilmadi")
        return self.match_repo.get_by_tournament(tournament_id)

    def record_match_result(self, match_id: int, home_score: int, away_score: int) -> Match:
        match = self.match_repo.get_by_id(match_id)
        if not match:
            raise LookupError(f"ID={match_id} bo'lgan uchrashuv topilmadi")
        match.record_result(home_score=home_score, away_score=away_score)
        updated = self.match_repo.update(match)

        if self.event_bus:
            self.event_bus.publish(
                MatchFinishedEvent(
                    tournament_id=updated.tournament_id,
                    match_id=updated.id,
                    home_team_id=updated.home_team_id,
                    away_team_id=updated.away_team_id,
                    home_score=updated.home_score,
                    away_score=updated.away_score,
                )
            )
        return updated

    def get_standings(self, tournament_id: int, scoring_rule: str = "standard") -> list[TeamStanding]:
        if not self.tournament_repo.get_by_id(tournament_id):
            raise LookupError(f"ID={tournament_id} bo'lgan turnir topilmadi")

        matches = self.match_repo.get_by_tournament(tournament_id)
        teams = self.team_repo.get_all()
        strategy = ScoringStrategyFactory.create(scoring_rule)
        return StandingsService(scoring_strategy=strategy).calculate(teams=teams, matches=matches)