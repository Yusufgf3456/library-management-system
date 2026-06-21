"""Database connection and schema setup.

Uses SQLite. Enables foreign key constraints on every connection and
creates the tables defined in schema.sql.
"""
import sqlite3
from pathlib import Path

# Locate the sql/ folder in the project root
BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
SEED_PATH = BASE_DIR / "sql" / "seed_data.sql"


class Database:
    """Manages the SQLite connection."""

    def __init__(self, db_path: str = "library.db"):
        """Connect to the database and create the schema.

        :param db_path: Path to the database file. Use ":memory:" for an
                        in-memory (temporary) database; used in tests.
        """
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        # Allow dict-like row access (row["title"])
        self.conn.row_factory = sqlite3.Row
        # Foreign key constraints are OFF by default in SQLite
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Run schema.sql to create the tables."""
        sql = SCHEMA_PATH.read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()

    def seed(self) -> None:
        """Load the sample data from seed_data.sql."""
        sql = SEED_PATH.read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()

    def close(self) -> None:
        """Close the connection."""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
