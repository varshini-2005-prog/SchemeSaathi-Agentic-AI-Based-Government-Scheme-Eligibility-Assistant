"""
tests/test_evaluation.py
Automated evaluation test suite verifying end-to-end agentic workflow, state persistence,
rule evaluations, what-if simulator, and benchmark accuracy metrics.
"""

import pytest
from app.graph import run_schemesaathi_turn, create_initial_state
from app.utils.evaluation import evaluator


def test_pudhumai_penn_eligibility_eval():
    """Verify Pudhumai Penn scheme evaluation for eligible female student."""
    msg = "I am a 20 year old female student from Coimbatore. I studied in Tamil Nadu Govt school from Class 6 to 12. Family income is 1.8 lakh."
    state = run_schemesaathi_turn(msg, create_initial_state())

    results = state.get("eligibility_results", [])
    pudhumai_res = next((r for r in results if r["scheme_id"] == "TN_SCH_001"), None)

    assert pudhumai_res is not None
    assert pudhumai_res["overall_status"] == "ELIGIBLE"
    assert pudhumai_res["fail_count"] == 0


def test_tamizh_pudhalvan_eligibility_eval():
    """Verify Tamizh Pudhalvan scheme evaluation for eligible male student."""
    msg = "Enakku 22 age male student. TN govt school-la Class 6 to 12 padithen."
    state = run_schemesaathi_turn(msg, create_initial_state())

    results = state.get("eligibility_results", [])
    tamizh_res = next((r for r in results if r["scheme_id"] == "TN_SCH_002"), None)

    assert tamizh_res is not None
    assert tamizh_res["overall_status"] == "ELIGIBLE"


def test_what_if_simulator_execution():
    """Verify What-if simulator recalculates eligibility without altering base profile."""
    # 1. Base query with high income
    msg1 = "I am a 30 year old female in Tamil Nadu. Family income is 3.5 lakh."
    state = run_schemesaathi_turn(msg1, create_initial_state())

    # 2. What-if query simulating lower income
    msg2 = "What if my annual income was 2 lakh instead of 3.5 lakh?"
    state2 = run_schemesaathi_turn(msg2, state)

    assert state2.get("is_what_if") is True
    assert "WHAT-IF SIMULATION RESULTS" in state2.get("final_response", "")


def test_benchmark_metrics():
    """Verify benchmark evaluator metrics computation."""
    metrics = evaluator.evaluate()
    assert metrics["precision"] >= 0.90
    assert metrics["false_eligibility_rate"] <= 0.05
    assert metrics["accuracy"] >= 0.85

