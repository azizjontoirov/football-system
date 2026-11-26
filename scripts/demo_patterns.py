from app.domain.entities.match import Match
from app.domain.entities.team import Team
from app.domain.services.standings_service import StandingsService
from app.domain.strategies.scoring_strategy import ScoringStrategyFactory


def print_table(title: str, standings):
    print(f"\n=== {title} ===")
    print(f"{'#':<3} {'Jamoa':<22} {'O':<3} {'G':<3} {'D':<3} {'M':<3} {'T/N':<6} {'Ochko':<5}")
    print("-" * 52)
    for idx, row in enumerate(standings, start=1):
        gd = f"{row.goals_for}:{row.goals_against}"
        print(
            f"{idx:<3} {row.team_name:<22} {row.played:<3} {row.won:<3} "
            f"{row.drawn:<3} {row.lost:<3} {gd:<6} {row.points:<5}"
        )


def main():
    teams = [
        Team(id=1, name="Samarqand United", city="Samarqand"),
        Team(id=2, name="Registon FC", city="Samarqand"),
        Team(id=3, name="Zarafshon Havaskor", city="Samarqand"),
    ]

    m1 = Match(id=1, tournament_id=1, home_team_id=1, away_team_id=2)
    m1.record_result(home_score=3, away_score=1)  # Samarqand United 3 ta gol urdi (+1 bonus)

    m2 = Match(id=2, tournament_id=1, home_team_id=2, away_team_id=3)
    m2.record_result(home_score=3, away_score=3)  # Ikkala jamoa ham 3 tadan gol urdi (+1 bonus)

    # 1. Standart strategiya (Factory orqali)
    standard_strategy = ScoringStrategyFactory.create("standard")
    standard_table = StandingsService(scoring_strategy=standard_strategy).calculate(teams, [m1, m2])
    print_table("Standart qoida (3-1-0)", standard_table)

    # 2. Bonusli strategiya (Factory orqali)
    bonus_strategy = ScoringStrategyFactory.create("bonus")
    bonus_table = StandingsService(scoring_strategy=bonus_strategy).calculate(teams, [m1, m2])
    print_table("Havaskor bonus qoidasi (3+ golga +1 ochko)", bonus_table)


if __name__ == "__main__":
    main()