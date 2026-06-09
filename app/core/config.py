from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm: str = "HS256"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()
