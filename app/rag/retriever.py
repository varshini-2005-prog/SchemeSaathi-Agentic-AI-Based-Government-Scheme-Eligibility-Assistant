"""
app/rag/retriever.py
FAISS vector index builder and retriever for SchemeSaathi.
Provides top-k document retrieval with scheme metadata filtering.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from app.rag.ingestion import ingestor
from app.rag.embeddings import embedder
from app.utils.logger import logger


class FAISSRetriever:
    """FAISS index manager and scheme evidence retriever."""

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.index: Optional[faiss.IndexFlatIP] = None
        self.is_built = False
        self.build_index()

    def build_index(self):
        """Ingests raw schemes, computes embeddings, and builds FAISS index."""
        self.chunks = ingestor.ingest_all_schemes()
        if not self.chunks:
            logger.warning("No document chunks available to build FAISS index.")
            return

        texts = [c["content"] for c in self.chunks]
        embeddings = embedder.embed_texts(texts)

        dimension = embeddings.shape[1]
        # Using IndexFlatIP (Inner Product) for cosine similarity on normalized vectors
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        self.is_built = True
        logger.info(f"Successfully built FAISS index with {self.index.ntotal} vectors.")

    def search(self, query: str, top_k: int = 3, scheme_id_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves top-k relevant document chunks for a query string.
        Supports metadata filtering by scheme_id.
        """
        if not self.is_built or self.index is None or not self.chunks:
            self.build_index()

        query_emb = embedder.embed_texts([query])
        scores, indices = self.index.search(query_emb, min(top_k * 3, len(self.chunks)))

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < 0 or idx >= len(self.chunks):
                continue
            chunk = self.chunks[idx]
            if scheme_id_filter and chunk["metadata"]["scheme_id"] != scheme_id_filter:
                continue

            results.append({
                "content": chunk["content"],
                "metadata": chunk["metadata"],
                "score": float(score),
            })
            if len(results) >= top_k:
                break

        return results


scheme_retriever = FAISSRetriever()
