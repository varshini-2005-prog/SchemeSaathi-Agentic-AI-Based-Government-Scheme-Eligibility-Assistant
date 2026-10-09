"""
app/config.py
Configuration loader for SchemeSaathi using Pydantic.
Reads environment variables with sensible defaults for Phase 1.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


class Settings:
    """Central configuration class for application settings."""

    # Project metadata
    PROJECT_NAME: str = os.getenv("APP_NAME", "SchemeSaathi")
    VERSION: str = "0.1.0"
    ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Embedding & Vector Database
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    FAISS_INDEX_PATH: Path = BASE_DIR / os.getenv(
        "FAISS_INDEX_PATH", "data/processed/faiss_index"
    )

    # SQLite Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./schemesaathi.db")
    DB_PATH: Path = BASE_DIR / "schemesaathi.db"


settings = Settings()
