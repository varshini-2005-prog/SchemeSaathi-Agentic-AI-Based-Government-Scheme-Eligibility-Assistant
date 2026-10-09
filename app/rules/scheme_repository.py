"""
app/rules/scheme_repository.py
Scheme repository loader and data cleaner for SchemeSaathi.
Loads, validates, and indexes official scheme documents from data/raw/ directory.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from app.config import settings
from app.models.scheme import Scheme
from app.utils.logger import logger


class SchemeRepository:
    """Manages the in-memory registry of official government schemes loaded from disk."""

    def __init__(self, raw_data_dir: Optional[Path] = None):
        self.raw_data_dir = raw_data_dir or settings.RAW_DATA_DIR
        self._schemes: Dict[str, Scheme] = {}
        self.load_schemes()

    def load_schemes(self) -> int:
        """
        Loads all raw JSON scheme documents from data/raw/ directory.
        Validates content using Pydantic Scheme model.
        Returns the count of successfully loaded schemes.
        """
        self._schemes.clear()

        if not self.raw_data_dir.exists():
            logger.warning(f"Raw data directory does not exist at {self.raw_data_dir}")
            return 0

        json_files = list(self.raw_data_dir.glob("*.json"))
        logger.info(f"Found {len(json_files)} raw scheme files in {self.raw_data_dir}")

        for filepath in json_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                
                scheme = Scheme(**raw_data)
                self._schemes[scheme.scheme_id] = scheme
                logger.info(f"Loaded scheme: [{scheme.scheme_id}] {scheme.scheme_name}")
            except Exception as e:
                logger.error(f"Failed to parse scheme document at {filepath}: {e}")

        logger.info(f"Total schemes successfully loaded into repository: {len(self._schemes)}")
        return len(self._schemes)

    def get_all_schemes(self) -> List[Scheme]:
        """Returns list of all registered schemes."""
        return list(self._schemes.values())

    def get_scheme_by_id(self, scheme_id: str) -> Optional[Scheme]:
        """Retrieves a specific scheme by its scheme_id."""
        return self._schemes.get(scheme_id)

    def get_schemes_by_category(self, category_keyword: str) -> List[Scheme]:
        """Filter schemes by category keyword."""
        keyword_lower = category_keyword.lower()
        return [
            s for s in self._schemes.values()
            if keyword_lower in s.scheme_category.lower()
        ]

    def get_schemes_by_level(self, level: str) -> List[Scheme]:
        """Filter schemes by government level (State, Central)."""
        level_lower = level.lower()
        return [
            s for s in self._schemes.values()
            if level_lower in s.government_level.lower()
        ]


# Singleton instance for global access
scheme_repository = SchemeRepository()
