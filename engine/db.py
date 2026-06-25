"""One-time database setup script. Safe to run multiple times."""

from engine.init_db import init_database

if __name__ == "__main__":
    init_database()
    print("Database initialized.")
