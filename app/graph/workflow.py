"""
app/graph/workflow.py
LangGraph workflow pipeline builder for SchemeSaathi.
Connects input processing, adaptive interviewing, deterministic eligibility evaluation,
source claim verification, document guidance, what-if simulation, and response formatting into a stateful graph.
"""

from langgraph.graph import StateGraph, START, END
from app.graph.state import SchemeState, create_initial_state
from app.agents import (
    input_processor,
    interviewer_agent,
    eligibility_agent,
    verifier_agent,
    document_agent,
    what_if_agent,
    response_generator,
)
from app.utils.logger import logger


def build_schemesaathi_graph() -> StateGraph:
    """Builds and compiles the master SchemeSaathi agentic workflow graph."""

    workflow = StateGraph(SchemeState)

    # 1. Add Nodes
    workflow.add_node("input_processor", input_processor.process_input)
    workflow.add_node("interviewer", interviewer_agent.generate_interview_question)
    workflow.add_node("eligibility_evaluator", eligibility_agent.evaluate_candidates)
    workflow.add_node("verifier", verifier_agent.verify_eligibility_claims)
    workflow.add_node("document_agent", document_agent.process_documents_and_steps)
    workflow.add_node("what_if_simulator", what_if_agent.run_simulation)
    workflow.add_node("response_generator", response_generator.format_final_response)

    # 2. Add Sequential Edges
    workflow.add_edge(START, "input_processor")
    workflow.add_edge("input_processor", "interviewer")
    workflow.add_edge("interviewer", "eligibility_evaluator")
    workflow.add_edge("eligibility_evaluator", "verifier")
    workflow.add_edge("verifier", "document_agent")
    workflow.add_edge("document_agent", "what_if_simulator")
    workflow.add_edge("what_if_simulator", "response_generator")
    workflow.add_edge("response_generator", END)

    app = workflow.compile()
    logger.info("Compiled LangGraph SchemeSaathi workflow graph successfully.")
    return app


schemesaathi_app = build_schemesaathi_graph()


def run_schemesaathi_turn(user_message: str, current_state: SchemeState = None) -> SchemeState:
    """
    Executes a single multi-turn interaction through the LangGraph workflow.
    Preserves state across calls.
    """
    if current_state is None:
        current_state = create_initial_state()

    current_state["user_message"] = user_message
    updated_state = schemesaathi_app.invoke(current_state)
    return updated_state
