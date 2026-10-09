"""
app/agents/input_processor.py
Input Processor & Natural Language NLU Agent for SchemeSaathi.
Parses user messages in Tamil, English, and Tanglish (Tamil-English mix).
Detects language and extracts structured user profile attributes.
"""

import re
from typing import Dict, Any, Tuple
from app.graph.state import SchemeState
from app.rules.parser import normalizer
from app.utils.logger import logger


class InputProcessorAgent:
    """Natural Language Understanding agent for Tamil, English, and Tanglish queries."""

    def detect_language(self, text: str) -> str:
        """
        Detects whether text is Tamil script ('ta'), Tanglish ('ta-en'), or English ('en').
        """
        # Tamil script Unicode range: U+0B80 to U+0BFF
        tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", text))
        if tamil_chars > 3:
            return "ta"

        # Tanglish keywords check
        tanglish_words = ["enakku", "enakkum", "irukken", "irukku", "vayasu", "naan", "la", "panren", "kidaikkum", "enna", "varumanam"]
        words = text.lower().split()
        if any(w in words for w in tanglish_words):
            return "ta-en"

        return "en"

    def extract_profile_attributes(self, text: str, existing_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts age, income, district, occupation, education, land, etc., from input string.
        Preserves existing known values unless overridden.
        """
        profile = dict(existing_profile)
        s = text.lower()

        # 1. Age extraction
        # e.g., "24 age", "24 vayasu", "age 24", "24 years"
        age_match = re.search(r"\b(\d{1,2})\s*(?:age|vayasu|years|yrs|வயது)?\b", s)
        if age_match:
            num = int(age_match.group(1))
            if 15 <= num <= 90:
                profile["age"] = num

        # 2. Family Income extraction
        # e.g., "1.8 lakh", "1,80,000", "2 lakh", "1.8L"
        income = normalizer.parse_income(s)
        if income is not None and income > 1000:
            profile["annual_family_income"] = income

        # 3. District extraction
        districts = ["coimbatore", "chennai", "madurai", "trichy", "salem", "tirunelveli", "erode", "vellore", "thanjavur", "kanchipuram"]
        for dist in districts:
            if dist in s:
                profile["district"] = dist.capitalize()

        # 4. Gender extraction
        gender = normalizer.parse_gender(s)
        if gender:
            profile["gender"] = gender

        # 5. Occupation & Education extraction
        if any(w in s for w in ["student", "studying", "padikkiren", "college", "school"]):
            profile["occupation"] = "student"
            profile["education_status"] = "pursuing_higher_education"

        if any(w in s for w in ["farmer", "vivasaayi", "agri", "agriculture"]):
            profile["occupation"] = "farmer"

        # 6. Schooling (TN Govt School Class 6 to 12)
        if any(w in s for w in ["govt school", "arasu palli", "government school", "class 6", "6 to 12", "6th to 12th"]):
            profile["govt_school_study_class_6_to_12"] = True

        # 7. Land ownership
        if any(w in s for w in ["land", "nilam", "agricultural land"]):
            if any(w in s for w in ["no", "illai", "ille"]):
                profile["land_ownership"] = False
            else:
                profile["land_ownership"] = True

        return profile

    def process_input(self, state: SchemeState) -> SchemeState:
        """
        Node function that processes user message, updates language and profile state.
        """
        user_msg = state.get("user_message", "")
        existing_profile = state.get("profile", {})

        lang = self.detect_language(user_msg)
        state["language"] = lang

        updated_profile = self.extract_profile_attributes(user_msg, existing_profile)
        state["profile"] = updated_profile

        logger.info(f"Input Processor detected language '{lang}' and updated profile: {updated_profile}")
        return state


input_processor = InputProcessorAgent()
