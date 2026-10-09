"""
run.py
Main entry point script for SchemeSaathi Phase 1.
Initializes the system, runs health checks, and logs basic system metrics.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.config import settings
from app.utils.logger import logger
from app.database import init_db
from app.models.schemas import SystemStatusResponse
from app.rules import scheme_repository


def check_system_health() -> SystemStatusResponse:
    """Performs startup checks for database, directory structure, and scheme repository."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENV}]")
    
    # Initialize database tables
    db_ok = init_db()
    
    # Check directory structure
    dirs_ok = settings.RAW_DATA_DIR.exists() and settings.PROCESSED_DATA_DIR.exists()
    
    # Check Scheme Repository
    schemes_count = scheme_repository.load_schemes()

    status = "healthy" if (db_ok and dirs_ok and schemes_count >= 6) else "degraded"
    
    response = SystemStatusResponse(
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status=status,
        environment=settings.ENV,
        database_connected=db_ok,
        directories_ready=dirs_ok,
        details={
            "database_path": str(settings.DB_PATH),
            "raw_data_dir": str(settings.RAW_DATA_DIR),
            "processed_data_dir": str(settings.PROCESSED_DATA_DIR),
            "schemes_loaded_count": schemes_count,
            "llm_provider": settings.LLM_PROVIDER,
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
        }
    )
    
    return response



if __name__ == "__main__":
    health = check_system_health()
    logger.info(f"System Health Status: {health.status.upper()}")
    logger.info(f"Details: {health.details}")
    print("\n==================================================")
    print(f"  {health.app_name} v{health.version} Initialized Successfully!")
    print("==================================================")
    print("To run tests:           pytest tests/")
    print("To run Streamlit UI:     streamlit run frontend/streamlit_app.py")
    print("==================================================\n")
