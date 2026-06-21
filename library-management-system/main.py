"""Application entry point.

To run:  python main.py
To start with sample data on first run:  python main.py --seed
"""
import sys

from src.database import Database
from src.services import LibraryService
from src.cli import LibraryCLI

DB_FILE = "library.db"


def main() -> None:
    db = Database(DB_FILE)

    # If --seed is passed and the database is empty, load the sample data
    if "--seed" in sys.argv:
        existing = db.conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if existing == 0:
            db.seed()
            print("Sample data loaded.\n")
        else:
            print("Database already populated, sample data not loaded.\n")

    service = LibraryService(db)
    cli = LibraryCLI(service)
    try:
        cli.run()
    finally:
        db.close()


if __name__ == "__main__":
    main()
