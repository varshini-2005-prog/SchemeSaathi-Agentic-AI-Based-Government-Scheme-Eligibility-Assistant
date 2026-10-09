"""
app/rules/evaluator.py
Deterministic rule evaluation engine for SchemeSaathi.
Evaluates individual conditions against user profiles with PASS, FAIL, or UNKNOWN results.
Enforces 3-way decision logic (ELIGIBLE, NOT ELIGIBLE, NEED MORE INFORMATION).
"""

from typing import Dict, Any, List, Tuple
from app.models.scheme import Scheme, EligibilityRule
from app.utils.logger import logger


class RuleEvaluationResult:
    """Evaluation result for a single rule."""
    def __init__(self, rule: EligibilityRule, status: str, user_value: Any, reason: str):
        self.rule_id = rule.rule_id
        self.field = rule.field
        self.operator = rule.operator
        self.target_value = rule.target_value
        self.description = rule.description
        self.source = rule.source
        self.status = status  # "PASS", "FAIL", "UNKNOWN"
        self.user_value = user_value
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "field": self.field,
            "operator": self.operator,
            "target_value": self.target_value,
            "description": self.description,
            "source": self.source,
            "status": self.status,
            "user_value": self.user_value,
            "reason": self.reason,
        }


class SchemeEligibilityEvaluator:
    """Evaluates a Scheme against a user profile dict."""

    def evaluate_rule(self, rule: EligibilityRule, profile: Dict[str, Any]) -> RuleEvaluationResult:
        """
        Evaluates a single rule against user profile attributes.
        Returns RuleEvaluationResult with status PASS, FAIL, or UNKNOWN.
        """
        user_val = profile.get(rule.field)

        # 1. Missing information -> UNKNOWN
        if user_val is None:
            return RuleEvaluationResult(
                rule=rule,
                status="UNKNOWN",
                user_value=None,
                reason=f"User value for '{rule.field}' is missing (UNKNOWN)."
            )

        op = rule.operator
        target = rule.target_value

        try:
            # 2. Operator logic evaluation
            if op == "equals":
                if str(user_val).strip().lower() == str(target).strip().lower():
                    return RuleEvaluationResult(rule, "PASS", user_val, f"Value matches required target ({target}).")
                else:
                    return RuleEvaluationResult(rule, "FAIL", user_val, f"Provided value '{user_val}' does not match required '{target}'.")

            elif op == "in":
                # target is a list of allowed values
                if isinstance(target, list):
                    normalized_target = [str(t).strip().lower() for t in target]
                    if str(user_val).strip().lower() in normalized_target:
                        return RuleEvaluationResult(rule, "PASS", user_val, f"Value '{user_val}' is in allowed values.")
                    else:
                        return RuleEvaluationResult(rule, "FAIL", user_val, f"Value '{user_val}' not in allowed values {target}.")
                elif str(user_val).strip().lower() in str(target).strip().lower():
                    return RuleEvaluationResult(rule, "PASS", user_val, f"Value '{user_val}' matches target pattern.")
                else:
                    return RuleEvaluationResult(rule, "FAIL", user_val, f"Value '{user_val}' does not match '{target}'.")

            elif op in ["less_than", "less_than_or_equal", "greater_than", "greater_than_or_equal"]:
                user_num = float(user_val)
                target_num = float(target)

                if op == "less_than":
                    passed = user_num < target_num
                elif op == "less_than_or_equal":
                    passed = user_num <= target_num
                elif op == "greater_than":
                    passed = user_num > target_num
                elif op == "greater_than_or_equal":
                    passed = user_num >= target_num

                status = "PASS" if passed else "FAIL"
                reason = f"Numeric value {user_num} is {status.lower()} against threshold {op} {target_num}."
                return RuleEvaluationResult(rule, status, user_val, reason)

            else:
                return RuleEvaluationResult(rule, "UNKNOWN", user_val, f"Unsupported rule operator '{op}'.")

        except (ValueError, TypeError) as e:
            logger.error(f"Type error evaluating rule {rule.rule_id} with user_value '{user_val}': {e}")
            return RuleEvaluationResult(rule, "UNKNOWN", user_val, f"Could not convert profile value '{user_val}' to numeric comparison.")

    def evaluate_scheme(self, scheme: Scheme, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates all rules for a scheme and computes overall eligibility status:
        - ELIGIBLE: All mandatory rules PASS
        - NOT ELIGIBLE: At least one mandatory rule FAILS
        - NEED MORE INFORMATION: No rule FAILS, but at least one rule is UNKNOWN
        """
        rule_results: List[RuleEvaluationResult] = []
        pass_count = 0
        fail_count = 0
        unknown_count = 0
        missing_fields = []

        for rule in scheme.eligibility_rules:
            res = self.evaluate_rule(rule, profile)
            rule_results.append(res)

            if res.status == "PASS":
                pass_count += 1
            elif res.status == "FAIL":
                fail_count += 1
            elif res.status == "UNKNOWN":
                unknown_count += 1
                if rule.field not in missing_fields:
                    missing_fields.append(rule.field)

        if fail_count > 0:
            overall_status = "NOT ELIGIBLE"
        elif unknown_count > 0:
            overall_status = "NEED MORE INFORMATION"
        else:
            overall_status = "ELIGIBLE"

        return {
            "scheme_id": scheme.scheme_id,
            "scheme_name": scheme.scheme_name,
            "overall_status": overall_status,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "unknown_count": unknown_count,
            "missing_fields": missing_fields,
            "rule_evaluations": [r.to_dict() for r in rule_results],
            "official_url": scheme.official_url,
            "source_document": scheme.source_document,
            "required_documents": scheme.required_documents,
            "benefits": scheme.benefits,
        }


rule_evaluator = SchemeEligibilityEvaluator()
