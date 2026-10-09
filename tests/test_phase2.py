"""
tests/test_phase2.py
Phase 2 automated unit test suite for Official Scheme Document Collection.
Validates loading, cleaning, Pydantic schema validation, and rule integrity across all 6 schemes.
"""

import pytest
from pathlib import Path
from app.config import settings
from app.rules import scheme_repository, SchemeRepository
from app.models.scheme import Scheme, EligibilityRule


def test_raw_scheme_files_exist():
    """Verify that all 6 expected scheme JSON documents exist in data/raw/."""
    expected_files = [
        "pudhumai_penn.json",
        "tamizh_pudhalvan.json",
        "kmut.json",
        "cmchis.json",
        "pm_kisan.json",
        "ignoaps.json",
    ]
    raw_dir = settings.RAW_DATA_DIR
    for filename in expected_files:
        filepath = raw_dir / filename
        assert filepath.exists(), f"Raw scheme file missing: {filename}"


def test_scheme_repository_loading():
    """Verify that repository loads at least 6 valid schemes."""
    repo = SchemeRepository()
    schemes = repo.get_all_schemes()
    assert len(schemes) >= 6, f"Expected at least 6 schemes, found {len(schemes)}"


def test_scheme_field_integrity():
    """Verify that every loaded scheme has complete, validated metadata."""
    repo = SchemeRepository()
    schemes = repo.get_all_schemes()

    for scheme in schemes:
        assert isinstance(scheme, Scheme)
        assert scheme.scheme_id, "scheme_id must not be empty"
        assert scheme.scheme_name, f"scheme_name missing for {scheme.scheme_id}"
        assert scheme.scheme_category, f"scheme_category missing for {scheme.scheme_id}"
        assert scheme.government_level in ["State", "Central", "Central-State Joint"], f"Invalid level for {scheme.scheme_id}"
        assert scheme.state, f"state missing for {scheme.scheme_id}"
        assert scheme.description, f"description missing for {scheme.scheme_id}"
        assert scheme.benefits, f"benefits missing for {scheme.scheme_id}"
        assert len(scheme.eligibility_rules) >= 1, f"At least 1 rule required for {scheme.scheme_id}"
        assert len(scheme.required_documents) >= 1, f"Documents list required for {scheme.scheme_id}"
        assert scheme.application_method, f"application_method missing for {scheme.scheme_id}"
        assert scheme.official_url.startswith("http"), f"official_url must start with http for {scheme.scheme_id}"
        assert scheme.source_document, f"source_document missing for {scheme.scheme_id}"
        assert scheme.last_verified_date, f"last_verified_date missing for {scheme.scheme_id}"


def test_rule_formatting_and_sources():
    """Verify that all rules specify field, operator, description, and source citation."""
    repo = SchemeRepository()
    schemes = repo.get_all_schemes()

    valid_operators = ["equals", "in", "less_than", "greater_than", "less_than_or_equal", "greater_than_or_equal"]

    for scheme in schemes:
        for rule in scheme.eligibility_rules:
            assert isinstance(rule, EligibilityRule)
            assert rule.rule_id, "rule_id cannot be empty"
            assert rule.field, f"Rule field cannot be empty in {rule.rule_id}"
            assert rule.operator in valid_operators, f"Invalid operator '{rule.operator}' in {rule.rule_id}"
            assert rule.description, f"Rule description missing in {rule.rule_id}"
            assert rule.source, f"Source citation missing in {rule.rule_id}"


def test_scheme_filtering():
    """Verify scheme filtering methods."""
    repo = SchemeRepository()

    # Category query
    women_schemes = repo.get_schemes_by_category("women")
    assert len(women_schemes) >= 2, "Expected at least 2 women schemes (KMUT & Pudhumai Penn)"

    # Level query
    central_schemes = repo.get_schemes_by_level("central")
    assert len(central_schemes) >= 2, "Expected central schemes (PM-KISAN, IGNOAPS)"

    # ID lookup
    pudhumai = repo.get_scheme_by_id("TN_SCH_001")
    assert pudhumai is not None
    assert pudhumai.scheme_name.startswith("Pudhumai Penn")
