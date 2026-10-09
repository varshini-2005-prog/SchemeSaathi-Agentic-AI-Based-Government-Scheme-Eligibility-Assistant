"""
app/agents/what_if.py
What-If Eligibility Simulator Agent for SchemeSaathi.
Allows users to simulate alternative scenarios (e.g. income = 2 lakh instead of 3 lakh)
by creating a temporary state without modifying the user's permanent profile.
"""

from typing import Dict, Any, Tuple
import copy
from app.graph.state import SchemeState
from app.rules.parser import normalizer
from app.agents.eligibility import eligibility_agent
from app.utils.logger import logger


class WhatIfSimulatorAgent:
    """Agent that performs counterfactual eligibility simulations."""

    def parse_what_if_query(self, query: str) -> Dict[str, Any]:
        """
        Parses counterfactual query strings for modified profile attributes.
        E.g. 'What if my income was 2 lakh instead of 3 lakh?' -> {'annual_family_income': 200000.0}
        """
        s = query.lower()

        # Only activate what-if parsing if explicit trigger phrases are present
        what_if_triggers = ["what if", "what-if", "suppose", "if my", "irundha", "irundhal"]
        if not any(t in s for t in what_if_triggers):
            return {}

        changes = {}


        # Check for income change
        if "income" in s or "வருமானம்" in s:
            income = normalizer.parse_income(s)
            if income is not None:
                changes["annual_family_income"] = income

        # Check for age change
        if "age" in s or "வயது" in s:
            age = normalizer.parse_age(s)
            if age is not None:
                changes["age"] = age

        # Check for land change
        if "land" in s or "நிலம்" in s:
            if "no" in s or "illai" in s or "0" in s:
                changes["land_ownership"] = False
                changes["wet_land_acres"] = 0.0
            elif "acres" in s or "acre" in s:
                num = normalizer.parse_age(s)
                if num is not None:
                    changes["wet_land_acres"] = float(num)

        return changes

    def run_simulation(self, state: SchemeState) -> SchemeState:
        """
        Runs counterfactual simulation on a temporary state copy.
        Compares baseline eligibility vs what-if eligibility.
        Preserves original state profile intact.
        """
        query = state.get("user_message", "")
        what_if_changes = self.parse_what_if_query(query)

        if not what_if_changes:
            state["is_what_if"] = False
            return state

        state["is_what_if"] = True
        state["what_if_changes"] = what_if_changes

        # 1. Store baseline eligibility
        baseline_results = copy.deepcopy(state.get("eligibility_results", []))

        # 2. Create temporary hypothetical profile
        hypothetical_profile = copy.deepcopy(state.get("profile", {}))
        for key, val in what_if_changes.items():
            hypothetical_profile[key] = val

        # 3. Create temporary state and re-evaluate eligibility
        temp_state: SchemeState = copy.deepcopy(state)
        temp_state["profile"] = hypothetical_profile
        temp_state = eligibility_agent.evaluate_candidates(temp_state)

        what_if_results = temp_state.get("eligibility_results", [])

        # 4. Generate delta comparison report
        comparison_lines = ["🔄 **WHAT-IF SIMULATION RESULTS**\n"]
        comparison_lines.append(f"**Simulated Attribute Changes:** {what_if_changes}\n")

        for base in baseline_results:
            scheme_id = base["scheme_id"]
            scheme_name = base["scheme_name"]
            base_status = base["overall_status"]

            # Find matching what-if result
            what_res = next((w for w in what_if_results if w["scheme_id"] == scheme_id), None)
            if what_res:
                new_status = what_res["overall_status"]
                icon_base = "✅" if base_status == "ELIGIBLE" else ("❌" if base_status == "NOT ELIGIBLE" else "⚠️")
                icon_new = "✅" if new_status == "ELIGIBLE" else ("❌" if new_status == "NOT ELIGIBLE" else "⚠️")

                if base_status != new_status:
                    comparison_lines.append(
                        f"• **{scheme_name}**: Changed from {icon_base} `{base_status}` ➡️ {icon_new} `{new_status}`"
                    )
                else:
                    comparison_lines.append(
                        f"• **{scheme_name}**: Remains {icon_new} `{new_status}`"
                    )

        state["final_response"] = "\n".join(comparison_lines)
        logger.info(f"What-if Simulator executed for changes: {what_if_changes}")
        return state


what_if_agent = WhatIfSimulatorAgent()
