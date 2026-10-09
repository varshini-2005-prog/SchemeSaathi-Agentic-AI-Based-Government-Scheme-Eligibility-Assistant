"""
app/agents/eligibility.py
Eligibility Reasoner Agent for SchemeSaathi.
Evaluates user profile against every candidate scheme rule-by-rule.
Produces deterministic 3-way outcomes (ELIGIBLE, NOT ELIGIBLE, NEED MORE INFORMATION).
"""

from typing import Dict, Any, List
from app.graph.state import SchemeState
from app.rules.scheme_repository import scheme_repository
from app.rules.evaluator import rule_evaluator
from app.utils.logger import logger


class EligibilityReasonerAgent:
    """Evaluates candidate schemes rule-by-rule deterministically."""

    def evaluate_candidates(self, state: SchemeState) -> SchemeState:
        """
        Node function that processes candidate schemes against state profile.
        """
        profile = state.get("profile", {})
        candidates = state.get("candidate_schemes", [])

        if not candidates:
            all_schemes = scheme_repository.get_all_schemes()
            candidates = [s.dict() for s in all_schemes]
            state["candidate_schemes"] = candidates

        results = []
        for candidate_dict in candidates:
            scheme_id = candidate_dict.get("scheme_id")
            scheme = scheme_repository.get_scheme_by_id(scheme_id)

            if scheme:
                eval_res = rule_evaluator.evaluate_scheme(scheme, profile)
                results.append(eval_res)

        state["eligibility_results"] = results
        logger.info(f"Eligibility Reasoner evaluated {len(results)} schemes.")
        return state


eligibility_agent = EligibilityReasonerAgent()
