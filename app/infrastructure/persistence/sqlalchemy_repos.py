from sqlalchemy.orm import Session

from app.domain.entities.match import Match, MatchStatus
from app.domain.entities.player import Player
from app.domain.entities.team import Team
from app.domain.entities.tournament import Tournament, TournamentStatus
from app.domain.ports.match_repository import MatchRepositoryPort
from app.domain.ports.player_repository import PlayerRepositoryPort
from app.domain.ports.team_repository import TeamRepositoryPort
from app.domain.ports.tournament_repository import TournamentRepositoryPort
from app.infrastructure.database.models import (
    MatchModel,
    PlayerModel,
    TeamModel,
    TournamentModel,
)


class SQLAlchemyTeamRepository(TeamRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, name: str, city: str) -> Team:
        Team(id=0, name=name, city=city)  # Domain validatsiyasi
        db_team = TeamModel(name=name, city=city)
        try:
            self.db.add(db_team)
            self.db.commit()
            self.db.refresh(db_team)
            return Team(id=db_team.id, name=db_team.name, city=db_team.city)
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, team_id: int) -> Team | None:
        row = self.db.get(TeamModel, team_id)
        return Team(id=row.id, name=row.name, city=row.city) if row else None

    def get_all(self) -> list[Team]:
        rows = self.db.query(TeamModel).order_by(TeamModel.id).all()
        return [Team(id=r.id, name=r.name, city=r.city) for r in rows]

    def delete(self, team_id: int) -> bool:
        row = self.db.get(TeamModel, team_id)
        if not row:
            return False
        try:
            self.db.delete(row)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise


class SQLAlchemyPlayerRepository(PlayerRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, full_name: str, team_id: int, jersey_number: int, position: str) -> Player:
        Player(id=0, full_name=full_name, team_id=team_id, jersey_number=jersey_number, position=position)
        db_player = PlayerModel(
            full_name=full_name,
            team_id=team_id,
            jersey_number=jersey_number,
            position=position,
        )
        try:
            self.db.add(db_player)
            self.db.commit()
            self.db.refresh(db_player)
            return Player(
                id=db_player.id,
                full_name=db_player.full_name,
                team_id=db_player.team_id,
                jersey_number=db_player.jersey_number,
                position=db_player.position,
            )
        except Exception:
            self.db.rollback()
            raise

    def get_by_team(self, team_id: int) -> list[Player]:
        rows = self.db.query(PlayerModel).filter(PlayerModel.team_id == team_id).all()
        return [
            Player(
                id=r.id,
                full_name=r.full_name,
                team_id=r.team_id,
                jersey_number=r.jersey_number,
                position=r.position,
            )
            for r in rows
        ]


class SQLAlchemyTournamentRepository(TournamentRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, name: str, season: str) -> Tournament:
        db_t = TournamentModel(name=name, season=season, status=TournamentStatus.UPCOMING.value)
        try:
            self.db.add(db_t)
            self.db.commit()
            self.db.refresh(db_t)
            return Tournament(
                id=db_t.id,
                name=db_t.name,
                season=db_t.season,
                status=TournamentStatus(db_t.status),
            )
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, tournament_id: int) -> Tournament | None:
        row = self.db.get(TournamentModel, tournament_id)
        if not row:
            return None
        return Tournament(
            id=row.id, name=row.name, season=row.season, status=TournamentStatus(row.status)
        )

    def get_all(self) -> list[Tournament]:
        rows = self.db.query(TournamentModel).order_by(TournamentModel.id).all()
        return [
            Tournament(id=r.id, name=r.name, season=r.season, status=TournamentStatus(r.status))
            for r in rows
        ]


class SQLAlchemyMatchRepository(MatchRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, tournament_id: int, home_team_id: int, away_team_id: int) -> Match:
        Match(id=0, tournament_id=tournament_id, home_team_id=home_team_id, away_team_id=away_team_id)
        db_m = MatchModel(
            tournament_id=tournament_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            status=MatchStatus.SCHEDULED.value,
        )
        try:
            self.db.add(db_m)
            self.db.commit()
            self.db.refresh(db_m)
            return self._to_entity(db_m)
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, match_id: int) -> Match | None:
        row = self.db.get(MatchModel, match_id)
        return self._to_entity(row) if row else None

    def get_by_tournament(self, tournament_id: int) -> list[Match]:
        rows = self.db.query(MatchModel).filter(MatchModel.tournament_id == tournament_id).all()
        return [self._to_entity(r) for r in rows]

    def update(self, match: Match) -> Match:
        row = self.db.get(MatchModel, match.id)
        if not row:
            raise LookupError(f"ID={match.id} bo'lgan uchrashuv topilmadi")
        try:
            row.home_score = match.home_score
            row.away_score = match.away_score
            row.status = match.status.value
            self.db.commit()
            self.db.refresh(row)
            return self._to_entity(row)
        except Exception:
            self.db.rollback()
            raise

    @staticmethod
    def _to_entity(row: MatchModel) -> Match:
        return Match(
            id=row.id,
            tournament_id=row.tournament_id,
            home_team_id=row.home_team_id,
            away_team_id=row.away_team_id,
            home_score=row.home_score,
            away_score=row.away_score,
            status=MatchStatus(row.status),
        )