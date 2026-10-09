"""
tests/test_phase1.py
Phase 1 automated unit test suite.
Validates configuration, logging, database initialization, and system health status.
"""

import os
import pytest
from pathlib import Path
from app.config import settings
from app.utils.logger import logger
from app.database import init_db, get_db_connection
from run import check_system_health


def test_configuration_loading():
    """Verify that configuration attributes load properly."""
    assert settings.PROJECT_NAME == "SchemeSaathi"
    assert settings.VERSION == "0.1.0"
    assert settings.ENV in ["development", "production", "testing"]
    assert isinstance(settings.BASE_DIR, Path)


def test_directory_structure():
    """Verify essential directories exist."""
    assert settings.RAW_DATA_DIR.exists(), "data/raw directory should exist"
    assert settings.PROCESSED_DATA_DIR.exists(), "data/processed directory should exist"


def test_logger_functionality():
    """Verify logger prints without raising exceptions."""
    try:
        logger.info("Test log message for Phase 1 verification.")
        success = True
    except Exception:
        success = False
    assert success, "Logger should function without errors"


def test_database_initialization():
    """Verify SQLite database initialization and table schema."""
    db_created = init_db()
    assert db_created is True, "Database initialization should return True"

    # Check tables exist
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "sessions" in tables, "sessions table should exist"
    assert "profiles" in tables, "profiles table should exist"
    assert "audit_logs" in tables, "audit_logs table should exist"


def test_system_health_check():
    """Verify check_system_health returns healthy response."""
    health_status = check_system_health()
    assert health_status.status == "healthy"
    assert health_status.database_connected is True
    assert health_status.directories_ready is True
