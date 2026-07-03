"""
Configuration for FinancePilot.

This module defines filesystem paths and the database URL used by the
application. Keeping configuration in one place makes it easier to change
how the app is run (for example, switching to PostgreSQL for production).
"""
from pathlib import Path

# BASE_DIR points to the package root (one level up from this file).
BASE_DIR = Path(__file__).resolve().parents[1]

# The SQLite file that will be created next to the `app/` package.
# In development we use SQLite for simplicity; production may use a different
# DATABASE_URL (for example a PostgreSQL connection string).
SQLITE_PATH = BASE_DIR / "financepilot.db"

# SQLAlchemy database URL. Sqlite uses the `sqlite:///` prefix with a file
# path. Other backends will require a different URL.
DATABASE_URL = f"sqlite:///{SQLITE_PATH}"
