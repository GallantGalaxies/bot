from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentVariablesSchema(BaseSettings):
    """TypedDict type to validate env vars."""

    DISCORD_BOT_TOKEN: str = Field(min_length=1)
    DEBUG: bool = False
    GUILD_ID: int = 1262692570954465312
    LOGGING_LEVEL: Literal["INFO", "DEBUG", "WARNING"] = "INFO"
    PROJECT_ROOT: Path = Path(__file__).parent

    def __init__(self) -> None:
        super().__init__()
        self.PROJECT_ROOT = Path(__file__).parent


env = EnvironmentVariablesSchema()
