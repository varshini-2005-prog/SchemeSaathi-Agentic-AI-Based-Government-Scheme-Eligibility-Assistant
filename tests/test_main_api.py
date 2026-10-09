"""
tests/test_main_api.py
Test suite for FastAPI REST API endpoints (/api/schemes, /api/evaluate, /api/whatif, /api/chat).
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["schemes_loaded"] >= 6


def test_get_all_schemes_endpoint():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) >= 6
    assert any(s["scheme_id"] == "TN_SCH_001" for s in schemes)


def test_evaluate_endpoint():
    payload = {
        "profile": {
            "age": 20,
            "gender": "female",
            "annual_family_income": 180000.0,
            "occupation": "student",
            "education_status": "pursuing_higher_education",
            "govt_school_study_class_6_to_12": True
        }
    }
    response = client.post("/api/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "eligibility_results" in data
    assert any(r["scheme_id"] == "TN_SCH_001" and r["overall_status"] == "ELIGIBLE" for r in data["eligibility_results"])


def test_whatif_endpoint():
    payload = {
        "baseline_profile": {
            "age": 24,
            "gender": "female",
            "annual_family_income": 350000.0
        },
        "simulated_changes": {
            "annual_family_income": 200000.0
        }
    }
    response = client.post("/api/whatif", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "comparison" in data
    assert data["simulated_profile"]["annual_family_income"] == 200000.0
    assert data["baseline_profile"]["annual_family_income"] == 350000.0
