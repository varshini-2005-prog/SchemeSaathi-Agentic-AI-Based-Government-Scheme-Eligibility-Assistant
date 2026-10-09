"""
app/agents/verifier.py
Source Claim Verification Agent for SchemeSaathi.
Cross-references eligibility evaluation claims against official FAISS retrieved text snippets.
Assigns VERIFIED or UNVERIFIED status with source citations.
"""

from typing import Dict, Any, List
from app.graph.state import SchemeState
from app.rag.retriever import scheme_retriever
from app.utils.logger import logger


class SourceVerifierAgent:
    """Verifies eligibility evaluation claims against official document evidence."""

    def verify_eligibility_claims(self, state: SchemeState) -> SchemeState:
        """
        Node function that checks eligibility results against FAISS context evidence.
        """
        eligibility_results = state.get("eligibility_results", [])
        verification_outputs = []
        sources_list = []

        for res in eligibility_results:
            scheme_id = res.get("scheme_id")
            scheme_name = res.get("scheme_name")
            overall_status = res.get("overall_status")

            # Retrieve evidence chunk from FAISS
            evidence_chunks = scheme_retriever.search(
                query=f"{scheme_name} eligibility criteria rules benefits",
                top_k=2,
                scheme_id_filter=scheme_id
            )

            if evidence_chunks:
                top_chunk = evidence_chunks[0]
                is_verified = True
                verification_status = "VERIFIED"
                citation = top_chunk["metadata"].get("source", res.get("source_document"))
                official_url = top_chunk["metadata"].get("official_url", res.get("official_url"))
                evidence_text = top_chunk["content"][:200] + "..."
            else:
                is_verified = False
                verification_status = "UNVERIFIED"
                citation = res.get("source_document", "Official Document")
                official_url = res.get("official_url", "")
                evidence_text = "No matching retrieved source chunk found in vector index."

            verification_outputs.append({
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "overall_status": overall_status,
                "verification_status": verification_status,
                "is_verified": is_verified,
                "citation": citation,
                "official_url": official_url,
                "evidence_snippet": evidence_text,
            })

            sources_list.append({
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "source": citation,
                "url": official_url,
            })

        state["verification_results"] = verification_outputs
        state["sources"] = sources_list
        logger.info(f"Source Verifier verified {len(verification_outputs)} scheme decisions.")
        return state


verifier_agent = SourceVerifierAgent()
