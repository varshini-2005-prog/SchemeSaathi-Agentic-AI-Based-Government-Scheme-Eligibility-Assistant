"""
app/database/connection.py
SQLite connection manager and database initialization helper for SchemeSaathi.
Stores session history, user profiles, and evaluation logs.
"""

import sqlite3
from pathlib import Path
from app.config import settings
from app.utils.logger import logger


def get_db_connection() -> sqlite3.Connection:
    """Returns a connected SQLite database instance."""
    db_path = settings.DB_PATH
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> bool:
    """
    Initializes necessary SQLite database tables for session state and profile management.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Session metadata table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT DEFAULT 'en'
            );
        """)

        # User Profile store table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                session_id TEXT PRIMARY KEY,
                profile_data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
        """)

        # Evaluation & Audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        conn.close()
        logger.info(f"SQLite database initialized successfully at: {settings.DB_PATH}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize SQLite database: {e}")
        return False
