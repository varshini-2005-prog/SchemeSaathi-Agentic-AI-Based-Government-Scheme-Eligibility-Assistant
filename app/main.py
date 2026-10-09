"""
app/main.py
FastAPI Web Server Backend for SchemeSaathi.
Exposes RESTful endpoints for health checks, scheme catalog, structured eligibility evaluations,
stateful multi-turn agent chats, and what-if eligibility simulations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import json
import copy

from app.config import settings
from app.utils.logger import logger
from app.database import get_db_connection, init_db
from app.graph import run_schemesaathi_turn, create_initial_state, SchemeState
from app.rules import scheme_repository
from app.agents import eligibility_agent, verifier_agent, document_agent, what_if_agent

app = FastAPI(
    title="SchemeSaathi API",
    description="Tamil + English Agentic Government Scheme Eligibility Assistant Backend",
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initializes SQLite database and scheme repository on startup."""
    init_db()
    scheme_repository.load_schemes()
    logger.info("SchemeSaathi FastAPI Backend Started.")


# --- Request / Response Models ---

class ChatRequest(BaseModel):
    session_id: str = "default_session"
    message: str


class EvaluateRequest(BaseModel):
    profile: Dict[str, Any]
    session_id: Optional[str] = "web_session"


class WhatIfRequest(BaseModel):
    baseline_profile: Dict[str, Any]
    simulated_changes: Dict[str, Any]


class ChatResponse(BaseModel):
    session_id: str
    language: str
    final_response: str
    profile: Dict[str, Any]
    eligibility_results: List[Dict[str, Any]]
    verification_results: List[Dict[str, Any]]
    missing_fields: List[str]


# --- Endpoints ---

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "healthy",
        "schemes_loaded": len(scheme_repository.get_all_schemes()),
    }


@app.get("/api/schemes")
def get_all_schemes():
    """Returns all loaded official government schemes with full metadata & rules."""
    schemes = scheme_repository.get_all_schemes()
    return [s.model_dump() if hasattr(s, "model_dump") else s.__dict__ for s in schemes]


@app.post("/api/evaluate")
def evaluate_profile(req: EvaluateRequest):
    """
    Direct structured profile evaluation endpoint.
    Processes user profile against all candidate schemes using Rule Engine & Verifier Agent.
    """
    state = create_initial_state(req.session_id or "web_session")
    state["profile"].update(req.profile)

    # Execute workflow nodes directly for structured form inputs
    state = eligibility_agent.evaluate_candidates(state)
    state = verifier_agent.verify_eligibility_claims(state)
    state = document_agent.process_documents_and_steps(state)

    # Compute missing fields
    candidates = state.get("candidate_schemes", [])
    missing = []
    for candidate in candidates:
        scheme_id = candidate.get("scheme_id")
        scheme = scheme_repository.get_scheme_by_id(scheme_id)
        if scheme:
            for rule in scheme.eligibility_rules:
                if state["profile"].get(rule.field) is None and rule.field not in missing:
                    missing.append(rule.field)

    state["missing_fields"] = missing

    return {
        "profile": state["profile"],
        "eligibility_results": state.get("eligibility_results", []),
        "verification_results": state.get("verification_results", []),
        "required_documents": state.get("required_documents", []),
        "next_steps": state.get("next_steps", []),
        "missing_fields": missing,
        "sources": state.get("sources", []),
    }


@app.post("/api/whatif")
def simulate_whatif(req: WhatIfRequest):
    """
    Runs counterfactual eligibility simulation comparing baseline profile vs simulated profile.
    Does not mutate baseline profile.
    """
    # 1. Baseline Evaluation
    base_state = create_initial_state("baseline_sim")
    base_state["profile"].update(req.baseline_profile)
    base_state = eligibility_agent.evaluate_candidates(base_state)
    base_results = base_state.get("eligibility_results", [])

    # 2. Simulated Evaluation
    sim_profile = copy.deepcopy(req.baseline_profile)
    sim_profile.update(req.simulated_changes)

    sim_state = create_initial_state("simulated_sim")
    sim_state["profile"].update(sim_profile)
    sim_state = eligibility_agent.evaluate_candidates(sim_state)
    sim_results = sim_state.get("eligibility_results", [])

    # 3. Delta Comparison
    comparison = []
    for b in base_results:
        s_id = b["scheme_id"]
        s_name = b["scheme_name"]
        b_status = b["overall_status"]

        matching_sim = next((s for s in sim_results if s["scheme_id"] == s_id), None)
        sim_status = matching_sim["overall_status"] if matching_sim else "N/A"

        comparison.append({
            "scheme_id": s_id,
            "scheme_name": s_name,
            "baseline_status": b_status,
            "simulated_status": sim_status,
            "status_changed": b_status != sim_status,
        })

    return {
        "baseline_profile": req.baseline_profile,
        "simulated_profile": sim_profile,
        "simulated_changes": req.simulated_changes,
        "comparison": comparison,
        "baseline_results": base_results,
        "simulated_results": sim_results,
    }


@app.post("/api/chat", response_model=ChatResponse)
def process_chat(req: ChatRequest):
    """
    Main stateful API endpoint for processing multi-turn agent interactions.
    Persists profile in SQLite database per session_id.
    """
    session_id = req.session_id
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT profile_data FROM profiles WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()

    current_state = create_initial_state(session_id)
    if row:
        try:
            saved_profile = json.loads(row["profile_data"])
            current_state["profile"] = saved_profile
        except Exception as e:
            logger.error(f"Error parsing saved profile for session {session_id}: {e}")

    updated_state = run_schemesaathi_turn(req.message, current_state)

    updated_profile_json = json.dumps(updated_state.get("profile", {}))
    cursor.execute("""
        INSERT INTO profiles (session_id, profile_data)
        VALUES (?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            profile_data = excluded.profile_data,
            updated_at = CURRENT_TIMESTAMP
    """, (session_id, updated_profile_json))
    conn.commit()
    conn.close()

    return ChatResponse(
        session_id=session_id,
        language=updated_state.get("language", "en"),
        final_response=updated_state.get("final_response", ""),
        profile=updated_state.get("profile", {}),
        eligibility_results=updated_state.get("eligibility_results", []),
        verification_results=updated_state.get("verification_results", []),
        missing_fields=updated_state.get("missing_fields", []),
    )


# Mount compiled React frontend SPA if frontend/dist exists
from fastapi.staticfiles import StaticFiles
from pathlib import Path

frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")

