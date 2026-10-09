"""
app/graph/state.py
LangGraph workflow state definition for SchemeSaathi.
Defines strongly typed SchemeState dict persisting across multi-turn interview conversations.
"""

from typing import TypedDict, Dict, List, Any, Optional

class SchemeState(TypedDict, total=False):
    """
    Core state object passed between nodes in the LangGraph workflow.
    """
    user_message: str
    language: str                        # "en", "ta", "ta-en" (Tanglish)
    session_id: str

    profile: Dict[str, Any]             # Current user profile attributes
    missing_fields: List[str]            # Fields required by candidate schemes that are missing

    candidate_schemes: List[Dict[str, Any]]    # Schemes currently being evaluated
    eligibility_results: List[Dict[str, Any]]  # Outcome per scheme (PASS/FAIL/UNKNOWN)
    verification_results: List[Dict[str, Any]] # Source verification outputs (VERIFIED/UNVERIFIED)

    required_documents: List[str]        # Aggregate list of required documents
    next_steps: List[str]                # Next step instructions for application

    what_if_changes: Dict[str, Any]      # Attributes changed in what-if simulation
    is_what_if: bool                     # Flag indicating what-if evaluation mode

    final_response: str                  # Rendered output message for user
    sources: List[Dict[str, Any]]        # Cited source documents
    errors: List[str]                    # Audit log of errors encountered


def create_initial_state(session_id: str = "default_session") -> SchemeState:
    """Helper factory function to create a clean, default state."""
    return {
        "user_message": "",
        "language": "en",
        "session_id": session_id,
        "profile": {
            "age": None,
            "gender": None,
            "district": None,
            "state_residence": "Tamil Nadu",
            "annual_family_income": None,
            "occupation": None,
            "education_status": None,
            "govt_school_study_class_6_to_12": None,
            "land_ownership": None,
            "wet_land_acres": None,
            "dry_land_acres": None,
            "four_wheeler_ownership": None,
            "annual_electricity_units": None,
            "is_institutional_landholder": None,
            "is_income_tax_payer": None,
            "is_bpl_or_destitute": None,
        },
        "missing_fields": [],
        "candidate_schemes": [],
        "eligibility_results": [],
        "verification_results": [],
        "required_documents": [],
        "next_steps": [],
        "what_if_changes": {},
        "is_what_if": False,
        "final_response": "",
        "sources": [],
        "errors": [],
    }
