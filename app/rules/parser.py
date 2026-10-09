"""
app/rules/parser.py
Profile attribute parser and value normalizer for SchemeSaathi.
Parses numeric values (lakhs, thousands), gender, occupation, and school types from multi-language text.
"""

import re
from typing import Dict, Any, Optional
from app.utils.logger import logger


class ProfileValueNormalizer:
    """Normalizes raw input strings into structured profile types."""

    @staticmethod
    def parse_income(text_val: Any) -> Optional[float]:
        """Converts strings like '1.8 lakh', '1,80,000', '2.5L' to float currency value."""
        if text_val is None:
            return None
        if isinstance(text_val, (int, float)):
            return float(text_val)

        s = str(text_val).lower().replace(",", "").replace("rs", "").replace("₹", "").strip()

        # Check for lakh / l
        lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|l)\b", s)
        if lakh_match:
            val = float(lakh_match.group(1))
            return val * 100000.0

        # Check for raw number
        num_match = re.search(r"(\d+(?:\.\d+)?)", s)
        if num_match:
            return float(num_match.group(1))

        return None

    @staticmethod
    def parse_age(text_val: Any) -> Optional[int]:
        """Extracts integer age from strings like '24 age', '24 years old', '24'."""
        if text_val is None:
            return None
        if isinstance(text_val, int):
            return text_val
        if isinstance(text_val, float):
            return int(text_val)

        s = str(text_val).lower().strip()
        num_match = re.search(r"(\d{1,3})", s)
        if num_match:
            return int(num_match.group(1))
        return None

    @staticmethod
    def parse_gender(text_val: Any) -> Optional[str]:
        """Normalizes gender to 'female' or 'male'."""
        if text_val is None:
            return None
        s = str(text_val).lower().strip()
        if any(w in s for w in ["female", "girl", "woman", "pen", "pombalai", "lady"]):
            return "female"
        if any(w in s for w in ["male", "boy", "man", "an", "aan", "gent"]):
            return "male"
        return None

    @staticmethod
    def parse_boolean(text_val: Any) -> Optional[bool]:
        """Converts yes/no, true/false, ama/illai to boolean."""
        if text_val is None:
            return None
        if isinstance(text_val, bool):
            return text_val
        s = str(text_val).lower().strip()
        if any(w in s for w in ["yes", "true", "ama", "aama", "aamam", "y", "1"]):
            return True
        if any(w in s for w in ["no", "false", "illai", "ille", "n", "0"]):
            return False
        return None


normalizer = ProfileValueNormalizer()
