from dataclasses import dataclass
from app.domain.entities.match import Match, MatchStatus
from app.domain.entities.team import Team
from app.domain.strategies.scoring_strategy import ScoringStrategy, StandardScoringStrategy


@dataclass
class TeamStanding:
    team_id: int
    team_name: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


class StandingsService:
    """Turnir jadvalini tanlangan strategiya asosida hisoblovchi xizmat."""

    def __init__(self, scoring_strategy: ScoringStrategy | None = None):
        self.scoring_strategy = scoring_strategy or StandardScoringStrategy()

    def calculate(self, teams: list[Team], matches: list[Match]) -> list[TeamStanding]:
        table: dict[int, TeamStanding] = {
            team.id: TeamStanding(team_id=team.id, team_name=team.name)
            for team in teams
        }

        for match in matches:
            if match.status != MatchStatus.FINISHED:
                continue

            home = table.get(match.home_team_id)
            away = table.get(match.away_team_id)
            if not home or not away:
                continue

            home.played += 1
            away.played += 1
            home.goals_for += match.home_score
            home.goals_against += match.away_score
            away.goals_for += match.away_score
            away.goals_against += match.home_score

            if match.home_score > match.away_score:
                home.won += 1
                away.lost += 1
            elif match.home_score < match.away_score:
                away.won += 1
                home.lost += 1
            else:
                home.drawn += 1
                away.drawn += 1

            # Ochkolar tanlangan Strategy orqali hisoblanadi
            home.points += self.scoring_strategy.calculate_points(match.home_score, match.away_score)
            away.points += self.scoring_strategy.calculate_points(match.away_score, match.home_score)

        return sorted(
            table.values(),
            key=lambda s: (s.points, s.goal_difference, s.goals_for),
            reverse=True,
        )