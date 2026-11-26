from abc import ABC, abstractmethod


class ScoringStrategy(ABC):
    """O'yin natijasiga ko'ra ochko hisoblash strategiyasi interfeysi."""

    @abstractmethod
    def calculate_points(self, goals_for: int, goals_against: int) -> int:
        pass


class StandardScoringStrategy(ScoringStrategy):
    """Standart FIFA qoidasi: g'alaba - 3, durang - 1, mag'lubiyat - 0."""

    def calculate_points(self, goals_for: int, goals_against: int) -> int:
        if goals_for > goals_against:
            return 3
        if goals_for == goals_against:
            return 1
        return 0


class BonusScoringStrategy(ScoringStrategy):
    """Havaskor liga bonus qoidasi: standart ochko + 3 va undan ko'p gol uchun +1 bonus."""

    def calculate_points(self, goals_for: int, goals_against: int) -> int:
        base_points = 3 if goals_for > goals_against else (1 if goals_for == goals_against else 0)
        bonus = 1 if goals_for >= 3 else 0
        return base_points + bonus


class ScoringStrategyFactory:
    """Turnir qoidasiga qarab mos strategiya obyektini yaratuvchi Fabrika."""

    _strategies: dict[str, type[ScoringStrategy]] = {
        "standard": StandardScoringStrategy,
        "bonus": BonusScoringStrategy,
    }

    @classmethod
    def create(cls, rule_type: str = "standard") -> ScoringStrategy:
        strategy_cls = cls._strategies.get(rule_type.lower())
        if not strategy_cls:
            allowed = ", ".join(cls._strategies.keys())
            raise ValueError(f"Noma'lum hisoblash qoidasi: '{rule_type}'. Mavjudlari: {allowed}")
        return strategy_cls()