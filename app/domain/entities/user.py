from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    VIEWER = "viewer"


@dataclass
class User:
    id: int
    username: str
    email: str
    role: UserRole = UserRole.VIEWER
