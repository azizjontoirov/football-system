from dataclasses import dataclass


@dataclass
class Team:
    id: int
    name: str
    city: str

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Jamoa nomi bo'sh bo'lishi mumkin emas")