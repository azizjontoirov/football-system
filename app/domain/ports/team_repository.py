from abc import ABC, abstractmethod
from app.domain.entities.team import Team


class TeamRepositoryPort(ABC):
    """Jamoalar ombori uchun chiquvchi port (interfeys)."""

    @abstractmethod
    def save(self, name: str, city: str) -> Team:
        pass

    @abstractmethod
    def get_all(self) -> list[Team]:
        pass
