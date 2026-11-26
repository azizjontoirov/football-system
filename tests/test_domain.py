import pytest

from app.domain.entities.match import Match, MatchStatus
from app.domain.entities.player import Player
from app.domain.entities.team import Team
from app.domain.events.football_events import TeamRegisteredEvent
from app.domain.services.standings_service import StandingsService
from app.domain.strategies.scoring_strategy import ScoringStrategyFactory
from app.infrastructure.messaging.in_memory_event_bus import InMemoryEventBus


def test_team_empty_name_raises_error():
    with pytest.raises(ValueError, match="Jamoa nomi"):
        Team(id=1, name="   ", city="Samarqand")


def test_player_invalid_jersey_number_raises_error():
    with pytest.raises(ValueError, match="1 dan 99 gacha"):
        Player(id=1, full_name="Azizbek Karimov", team_id=1, jersey_number=105, position="Hujumchi")


def test_match_same_team_raises_error():
    with pytest.raises(ValueError, match="o'ziga qarshi"):
        Match(id=1, tournament_id=1, home_team_id=1, away_team_id=1)


def test_match_negative_score_raises_error():
    match = Match(id=1, tournament_id=1, home_team_id=1, away_team_id=2)
    with pytest.raises(ValueError, match="manfiy"):
        match.record_result(home_score=-1, away_score=2)


def test_standings_standard_and_bonus_strategies():
    teams = [
        Team(id=1, name="Samarqand United", city="Samarqand"),
        Team(id=2, name="Registon FC", city="Samarqand"),
    ]
    match = Match(id=1, tournament_id=1, home_team_id=1, away_team_id=2)
    match.record_result(home_score=3, away_score=1)
    assert match.status == MatchStatus.FINISHED

    # Standart qoida (3-1-0)
    std_strategy = ScoringStrategyFactory.create("standard")
    std_table = StandingsService(scoring_strategy=std_strategy).calculate(teams, [match])
    assert std_table[0].team_name == "Samarqand United"
    assert std_table[0].points == 3
    assert std_table[0].goal_difference == 2

    # Bonusli qoida (3+ gol uchun +1 ochko)
    bonus_strategy = ScoringStrategyFactory.create("bonus")
    bonus_table = StandingsService(scoring_strategy=bonus_strategy).calculate(teams, [match])
    assert bonus_table[0].points == 4


def test_unknown_scoring_strategy_raises_error():
    with pytest.raises(ValueError, match="Noma'lum hisoblash qoidasi"):
        ScoringStrategyFactory.create("invalid_rule")


def test_event_bus_publish_and_subscribe():
    bus = InMemoryEventBus()
    received_events = []

    bus.subscribe(TeamRegisteredEvent, lambda event: received_events.append(event))
    bus.publish(TeamRegisteredEvent(team_id=1, team_name="Samarqand United", city="Samarqand"))

    assert len(received_events) == 1
    assert received_events[0].team_name == "Samarqand United"