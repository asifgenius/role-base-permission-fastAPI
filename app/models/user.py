from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    SUPER_ADMIN = "super_admin"
    MODERATOR = "moderator"
    REGULAR_USER = "regular_user"
    GUEST = "guest"


@dataclass(frozen=True)
class User:
    id: int
    role: Role
    email: str = ""
    password_hash: str = ""
