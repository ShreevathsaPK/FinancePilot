"""
Configuration for FinancePilot.

This module defines filesystem paths and the database URL used by the
application. Keeping configuration in one place makes it easier to change
how the app is run (for example, switching to PostgreSQL for production).
"""
import os
from pathlib import Path

# BASE_DIR points to the package root (one level up from this file).
BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


def _load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE pairs from a local .env file if present."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file(ENV_FILE)


def _get_env(key: str, default: str) -> str:
    """Return an environment value or a fallback default."""
    return os.getenv(key, default)


# The SQLite file that will be created next to the `app/` package.
# In development we use SQLite for simplicity; production may use a different
# DATABASE_URL (for example a PostgreSQL connection string).
SQLITE_PATH = Path(_get_env("SQLITE_PATH", str(BASE_DIR / "financepilot.db")))
if not SQLITE_PATH.is_absolute():
    SQLITE_PATH = (BASE_DIR / SQLITE_PATH).resolve()

# SQLAlchemy database URL. Sqlite uses the `sqlite:///` prefix with a file
# path. Other backends will require a different URL.
DATABASE_URL = _get_env("DATABASE_URL", f"sqlite:///{SQLITE_PATH}")
APP_TITLE = _get_env("APP_TITLE", "FinancePilot")
APP_VERSION = _get_env("APP_VERSION", "0.1.0")
APP_ENV = _get_env("APP_ENV", "development")
