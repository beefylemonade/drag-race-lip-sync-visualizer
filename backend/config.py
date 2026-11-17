"""Application configuration, loaded from environment variables.

Locally, values come from a .env file at the repo root. In production
(Render, Docker, GitHub Actions) they come from real environment variables.
"""
import os
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_VARS = ("GEMINI_API_KEY", "DATABASE_URL")


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


@dataclass(frozen=True)
class Settings:
    # repr=False keeps secrets out of logs if a Settings object is printed
    gemini_api_key: str = field(repr=False)
    database_url: str = field(repr=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and validate settings once; later calls return the same object."""
    # Real environment variables win over .env; a missing .env file is fine.
    load_dotenv(REPO_ROOT / ".env")
    missing = [n for n in REQUIRED_VARS if not os.environ.get(n, "").strip()]
    if missing:
        raise ConfigError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in the values."
        )
    return Settings(
        gemini_api_key=os.environ["GEMINI_API_KEY"].strip(),
        database_url=os.environ["DATABASE_URL"].strip(),
    )


def load_settings_or_exit() -> Settings:
    """For entry points: exit with a clear message instead of a traceback."""
    try:
        return get_settings()
    except ConfigError as err:
        sys.exit(f"Configuration error: {err}")


if __name__ == "__main__":
    load_settings_or_exit()
    print(f"Configuration OK ({len(REQUIRED_VARS)} variables loaded)")