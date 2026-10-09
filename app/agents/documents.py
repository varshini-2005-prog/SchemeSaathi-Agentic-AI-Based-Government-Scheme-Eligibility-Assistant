"""
app/agents/documents.py
Document Guidance and Application Next-Step Agent for SchemeSaathi.
Aggregates required documents for eligible or potential schemes and explains official procurement steps.
"""

from typing import Dict, Any, List
from app.graph.state import SchemeState
from app.rules.scheme_repository import scheme_repository
from app.utils.logger import logger

DOCUMENT_PROCUREMENT_MAP = {
    "Aadhaar Card": "Obtain / update at nearest Unique Identification Authority of India (UIDAI) Aadhaar Seva Kendra.",
    "Income Certificate": "Apply online at Tamil Nadu e-Sevai Portal (tnesevai.tn.gov.in) or local Revenue Tahsildar Office.",
    "Community Certificate": "Apply online at Tamil Nadu e-Sevai Portal (tnesevai.tn.gov.in) or local Tahsildar Office.",
    "Smart Family Card (Ration Card)": "Issued by Tamil Nadu Civil Supplies and Consumer Protection Department (tnpds.gov.in).",
    "School Transfer Certificate (Class 6 to 12 proof in TN Govt School)": "Obtain directly from the Headmaster / Principal of your TN Government School.",
    "Class 10th and 12th Marksheets / School TC": "Issued by Tamil Nadu Directorate of Government Examinations (DGE).",
    "College Admission Bonafide Certificate": "Issued by the Principal / Registrar of your higher education institution.",
    "Bank Account Details (Aadhaar Seeded)": "Open a savings bank account at any scheduled bank and link your Aadhaar number at the branch.",
    "Land Ownership Documents (Patta / Chitta / Land Revenue Record)": "Download official Patta/Chitta online via Tamil Nadu Anyal Patta Portal (eservices.tn.gov.in).",
    "BPL Card / Income & Destitute Certificate": "Issued by local Revenue Tahsildar Office (Social Security Scheme Wing)."
}


class DocumentAndNextStepAgent:
    """Agent that compiles mandatory documents and provides actionable application steps."""

    def process_documents_and_steps(self, state: SchemeState) -> SchemeState:
        """
        Node function that processes eligibility results and extracts document guidance.
        """
        eligibility_results = state.get("eligibility_results", [])
        all_required_docs = []
        next_steps = []

        for res in eligibility_results:
            status = res.get("overall_status")
            scheme_id = res.get("scheme_id")
            scheme = scheme_repository.get_scheme_by_id(scheme_id)

            if status in ["ELIGIBLE", "NEED MORE INFORMATION"] and scheme:
                for doc in scheme.required_documents:
                    if doc not in all_required_docs:
                        all_required_docs.append(doc)

                step_info = (
                    f"For {scheme.scheme_name}: Submit application via {scheme.application_method}. "
                    f"Official Web Portal: {scheme.official_url}"
                )
                if step_info not in next_steps:
                    next_steps.append(step_info)

        state["required_documents"] = all_required_docs
        state["next_steps"] = next_steps
        logger.info(f"Document Agent extracted {len(all_required_docs)} documents and {len(next_steps)} next steps.")
        return state


document_agent = DocumentAndNextStepAgent()
