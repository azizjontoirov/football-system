from app.domain.entities.match import Match
from app.domain.entities.player import Player
from app.domain.entities.team import Team
from app.domain.entities.tournament import Tournament, TournamentStatus
from app.domain.services.standings_service import StandingsService


def main():
    tournament = Tournament(
        id=1,
        name="Samarqand Havaskorlar Kubogi",
        season="2026",
        status=TournamentStatus.ACTIVE,
    )

    teams = [
        Team(id=1, name="Samarqand United", city="Samarqand"),
        Team(id=2, name="Registon FC", city="Samarqand"),
        Team(id=3, name="Zarafshon Havaskor", city="Samarqand"),
    ]

    player = Player(
        id=1, full_name="Azizbek Karimov", team_id=1, jersey_number=10, position="Hujumchi"
    )
    print(f"Turnir: {tournament.name} ({tournament.season})")
    print(f"Ro'yxatdan o'tgan o'yinchi: {player.full_name} (#{player.jersey_number}, {player.position})\n")

    # 3 ta o'yin yaratamiz va hisoblarni kiritamiz
    m1 = Match(id=1, tournament_id=1, home_team_id=1, away_team_id=2)
    m1.record_result(home_score=3, away_score=1)

    m2 = Match(id=2, tournament_id=1, home_team_id=2, away_team_id=3)
    m2.record_result(home_score=2, away_score=2)

    m3 = Match(id=3, tournament_id=1, home_team_id=3, away_team_id=1)
    m3.record_result(home_score=0, away_score=2)

    # Turnir jadvalini hisoblash
    standings = StandingsService().calculate(teams=teams, matches=[m1, m2, m3])

    print(f"{'#':<3} {'Jamoa':<22} {'O':<3} {'G':<3} {'D':<3} {'M':<3} {'T/N':<6} {'Ochko':<5}")
    print("-" * 52)
    for idx, row in enumerate(standings, start=1):
        gd = f"{row.goals_for}:{row.goals_against}"
        print(
            f"{idx:<3} {row.team_name:<22} {row.played:<3} {row.won:<3} "
            f"{row.drawn:<3} {row.lost:<3} {gd:<6} {row.points:<5}"
        )

    # Ichki qoida (validatsiya) ishlashini tekshirish
    print("\nBiznes-qoida tekshiruvi:")
    try:
        Match(id=4, tournament_id=1, home_team_id=1, away_team_id=1)
    except ValueError as err:
        print(f"Xatolik ushlandi -> {err}")


if __name__ == "__main__":
    main()