"""
app/rag/ingestion.py
Document ingestion and text chunking pipeline for official scheme documents.
Converts raw JSON scheme documents into text chunks with rich metadata for RAG indexing.
"""

from typing import List, Dict, Any
from app.models.scheme import Scheme
from app.rules.scheme_repository import scheme_repository
from app.utils.logger import logger


class SchemeDocumentIngestor:
    """Ingests official schemes and prepares searchable text chunks."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def scheme_to_chunks(self, scheme: Scheme) -> List[Dict[str, Any]]:
        """
        Converts a single Scheme object into multiple textual chunks with metadata.
        """
        chunks = []

        # 1. Summary Chunk
        summary_text = (
            f"Scheme Name: {scheme.scheme_name}\n"
            f"Scheme ID: {scheme.scheme_id}\n"
            f"Category: {scheme.scheme_category}\n"
            f"Government Level: {scheme.government_level} ({scheme.state})\n"
            f"Description: {scheme.description}\n"
            f"Benefits: {scheme.benefits}\n"
            f"Official Portal: {scheme.official_url}\n"
            f"Source Citation: {scheme.source_document}"
        )
        chunks.append({
            "content": summary_text,
            "metadata": {
                "scheme_id": scheme.scheme_id,
                "scheme_name": scheme.scheme_name,
                "section": "overview",
                "source": scheme.source_document,
                "official_url": scheme.official_url,
            }
        })

        # 2. Rules Chunk
        rules_text_lines = [f"Eligibility Rules for {scheme.scheme_name}:"]
        for rule in scheme.eligibility_rules:
            rules_text_lines.append(
                f"- Rule ID {rule.rule_id}: {rule.description}. "
                f"Field: {rule.field}, Condition: {rule.operator} {rule.target_value}. "
                f"Source: {rule.source}"
            )
        chunks.append({
            "content": "\n".join(rules_text_lines),
            "metadata": {
                "scheme_id": scheme.scheme_id,
                "scheme_name": scheme.scheme_name,
                "section": "eligibility_rules",
                "source": scheme.source_document,
                "official_url": scheme.official_url,
            }
        })

        # 3. Documents & Application Chunk
        docs_text = (
            f"Required Documents and Application Method for {scheme.scheme_name}:\n"
            f"Documents: {', '.join(scheme.required_documents)}\n"
            f"Application Method: {scheme.application_method}\n"
            f"Official Link: {scheme.official_url}"
        )
        chunks.append({
            "content": docs_text,
            "metadata": {
                "scheme_id": scheme.scheme_id,
                "scheme_name": scheme.scheme_name,
                "section": "documents_and_application",
                "source": scheme.source_document,
                "official_url": scheme.official_url,
            }
        })

        return chunks

    def ingest_all_schemes(self) -> List[Dict[str, Any]]:
        """Ingests all registered schemes from repository into chunks."""
        schemes = scheme_repository.get_all_schemes()
        all_chunks = []
        for scheme in schemes:
            chunks = self.scheme_to_chunks(scheme)
            all_chunks.extend(chunks)
        logger.info(f"Ingested {len(schemes)} schemes into {len(all_chunks)} text chunks.")
        return all_chunks



ingestor = SchemeDocumentIngestor()
