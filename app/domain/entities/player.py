from dataclasses import dataclass


@dataclass
class Player:
    id: int
    full_name: str
    team_id: int
    jersey_number: int
    position: str

    def __post_init__(self):
        if not self.full_name or not self.full_name.strip():
            raise ValueError("O'yinchi ism-familiyasi bo'sh bo'lishi mumkin emas")
        if not (1 <= self.jersey_number <= 99):
            raise ValueError("Futbolchi raqami 1 dan 99 gacha bo'lishi kerak")