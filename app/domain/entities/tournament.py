from dataclasses import dataclass
from enum import Enum


class TournamentStatus(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    FINISHED = "finished"


@dataclass
class Tournament:
    id: int
    name: str
    season: str
    status: TournamentStatus = TournamentStatus.UPCOMING