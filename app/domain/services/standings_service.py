from dataclasses import dataclass
from app.domain.entities.match import Match, MatchStatus
from app.domain.entities.team import Team


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
    """Turnir jadvalini hisoblash bo'yicha predmet sohasi xizmati."""

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
                home.points += 3
                away.lost += 1
            elif match.home_score < match.away_score:
                away.won += 1
                away.points += 3
                home.lost += 1
            else:
                home.drawn += 1
                away.drawn += 1
                home.points += 1
                away.points += 1

        return sorted(
            table.values(),
            key=lambda s: (s.points, s.goal_difference, s.goals_for),
            reverse=True,
        )