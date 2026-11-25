from dataclasses import dataclass
from enum import Enum


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    FINISHED = "finished"


@dataclass
class Match:
    id: int
    tournament_id: int
    home_team_id: int
    away_team_id: int
    home_score: int = 0
    away_score: int = 0
    status: MatchStatus = MatchStatus.SCHEDULED

    def __post_init__(self):
        if self.home_team_id == self.away_team_id:
            raise ValueError("Jamoa o'ziga qarshi o'ynashi mumkin emas")

    def record_result(self, home_score: int, away_score: int) -> None:
        if home_score < 0 or away_score < 0:
            raise ValueError("Gollar soni manfiy bo'lishi mumkin emas")
        self.home_score = home_score
        self.away_score = away_score
        self.status = MatchStatus.FINISHED

