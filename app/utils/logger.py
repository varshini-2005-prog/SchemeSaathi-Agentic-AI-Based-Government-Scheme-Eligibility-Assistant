"""
app/utils/logger.py
Centralized logging utility for SchemeSaathi.
Provides clean console logging for agent steps, API calls, and system status.
"""

import sys
import logging
from app.config import settings

def setup_logger(name: str = "schemesaathi") -> logging.Logger:
    """Configures and returns a standard logger instance."""
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if already configured
    if logger.handlers:
        return logger

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
