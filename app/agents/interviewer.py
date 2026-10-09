"""
app/agents/interviewer.py
Adaptive Interviewer Agent for SchemeSaathi.
Intelligently determines which missing profile attributes are required by candidate schemes
and asks ONLY relevant questions, avoiding redundant or irrelevant user prompts.
"""

from typing import Dict, Any, List
from app.graph.state import SchemeState
from app.rules.scheme_repository import scheme_repository
from app.utils.logger import logger


FIELD_QUESTION_MAP = {
    "en": {
        "age": "What is your age (in years)?",
        "gender": "What is your gender (Female / Male)?",
        "annual_family_income": "What is your total annual family income (in ₹ / Lakhs)?",
        "occupation": "What is your current occupation (e.g. Student, Farmer, Employed)?",
        "education_status": "Are you currently pursuing higher education (UG Degree, Diploma, or ITI)?",
        "govt_school_study_class_6_to_12": "Did you study from Class 6 to Class 12 in a Tamil Nadu Government School?",
        "land_ownership": "Do you or your family own cultivable agricultural land?",
        "four_wheeler_ownership": "Does your family own a four-wheeler vehicle (car / jeep)?",
        "annual_electricity_units": "Is your family's annual electricity consumption under 3,600 units?",
        "is_bpl_or_destitute": "Do you hold a Below Poverty Line (BPL) card or destitute certificate?",
    },
    "ta": {
        "age": "உங்கள் வயது என்ன?",
        "gender": "உங்கள் பாலினம் என்ன (பெண் / ஆண்)?",
        "annual_family_income": "உங்கள் குடும்பத்தின் ஆண்டு வருமானம் எவ்வளவு?",
        "occupation": "உங்கள் தற்போதைய தொழில் என்ன (மாணவர் / விவசாயி)?",
        "education_status": "நீங்கள் தற்போது உயர் கல்வி (டிகிரி / டிப்ளமோ / ITI) படிக்கிறீர்களா?",
        "govt_school_study_class_6_to_12": "நீங்கள் 6-ஆம் வகுப்பு முதல் 12-ஆம் வகுப்பு வரை அரசுப் பள்ளியில் படித்தீர்களா?",
        "land_ownership": "உங்களுக்கு சொந்தமாக விவசாய நிலம் உள்ளதா?",
        "four_wheeler_ownership": "உங்கள் குடும்பத்தில் கார் அல்லது நான்கு சக்கர வாகனம் உள்ளதா?",
        "annual_electricity_units": "உங்கள் குடும்ப மின்சார பயன்பாடு ஆண்டுக்கு 3,600 யூனிட்டிற்குள் உள்ளதா?",
        "is_bpl_or_destitute": "நீங்கள் வறுமைக் கோட்டிற்கு கீழ் உள்ளவரா (BPL Card)?",
    },
    "ta-en": {
        "age": "Ungal age enna?",
        "gender": "Ungal gender enna (Female / Male)?",
        "annual_family_income": "Ungal annual family income evvalavu (in Lakhs / Rupees)?",
        "occupation": "Ungal current occupation enna (e.g., Student, Farmer, Employed)?",
        "education_status": "Neengal ippo higher education (Degree / Diploma / ITI) padikkireengala?",
        "govt_school_study_class_6_to_12": "Class 6-la irundhu Class 12 varai TN Govt school-la paditheengala?",
        "land_ownership": "Ungalukku agricultural land irukkaa?",
        "four_wheeler_ownership": "Ungal family-la four-wheeler (car/jeep) irukkaa?",
        "annual_electricity_units": "Ungal annual electricity consumption 3,600 units-kku ulle irukkaa?",
        "is_bpl_or_destitute": "Ungalta BPL (Below Poverty Line) card irukkaa?",
    }
}


class AdaptiveInterviewerAgent:
    """Agent responsible for identifying relevant missing information and prompting user."""

    def select_candidate_schemes(self, profile: Dict[str, Any]) -> List[Any]:
        """
        Filters candidate schemes based on hard mismatches.
        E.g. if occupation == "student", exclude purely farmer-only schemes.
        """
        all_schemes = scheme_repository.get_all_schemes()
        candidates = []

        occupation = profile.get("occupation")
        gender = profile.get("gender")

        for scheme in all_schemes:
            # Skip farmer schemes if user explicitly states student/non-farmer
            if occupation and occupation.lower() == "student" and scheme.scheme_category == "Farmer Support":
                continue
            # Skip female-only schemes if male
            if gender and gender.lower() == "male" and "Women" in scheme.scheme_category and scheme.scheme_id == "TN_SCH_001":
                continue
            # Skip male-only schemes if female
            if gender and gender.lower() == "female" and scheme.scheme_id == "TN_SCH_002":
                continue

            candidates.append(scheme)

        return candidates

    def get_missing_required_fields(self, candidate_schemes: List[Any], profile: Dict[str, Any]) -> List[str]:
        """
        Identifies fields required by candidate schemes that are currently None in user profile.
        """
        missing = []
        for scheme in candidate_schemes:
            for rule in scheme.eligibility_rules:
                val = profile.get(rule.field)
                if val is None and rule.field not in missing:
                    missing.append(rule.field)
        return missing

    def generate_interview_question(self, state: SchemeState) -> SchemeState:
        """
        Main node function for adaptive interviewer.
        Updates state with missing_fields and next question if information is required.
        """
        profile = state.get("profile", {})
        language = state.get("language", "en")
        if language not in FIELD_QUESTION_MAP:
            language = "en"

        candidates = self.select_candidate_schemes(profile)
        state["candidate_schemes"] = [c.model_dump() if hasattr(c, "model_dump") else c.__dict__ for c in candidates]

        missing = self.get_missing_required_fields(candidates, profile)
        state["missing_fields"] = missing

        logger.info(f"Adaptive Interviewer identified {len(missing)} missing required fields: {missing}")

        return state


interviewer_agent = AdaptiveInterviewerAgent()
