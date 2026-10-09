"""
app/rag/embeddings.py
Multilingual embedding generator for SchemeSaathi.
Provides dense vector embeddings using SentenceTransformers with an offline TF-IDF fallback option.
"""

from typing import List
import numpy as np
from app.config import settings
from app.utils.logger import logger

class MultilingualEmbedder:
    """Generates embeddings for Tamil, English, and Tanglish text chunks."""

    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self.model = None
        self._init_model()

    def _init_model(self):
        """Attempts to load sentence-transformers model unless offline mode is set."""
        import os
        if os.getenv("USE_OFFLINE_EMBEDDINGS", "true").lower() == "true":
            logger.info("Using fast local TF-IDF vector embedder for multi-language matching.")
            self.model = None
            return

        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded sentence-transformers model: {self.model_name}")
        except Exception as e:
            logger.warning(f"SentenceTransformer '{self.model_name}' unavailable ({e}). Using fast offline TF-IDF vectorizer.")
            self.model = None



    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generates normalized vector embeddings for a list of strings."""
        if not texts:
            return np.empty((0, 384), dtype=np.float32)

        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                return embeddings.astype(np.float32)
            except Exception as e:
                logger.error(f"Error encoding with SentenceTransformer: {e}")

        # Fallback: simple token-frequency vector representation (384 dimensions)
        return self._tfidf_fallback_embed(texts)

    def _tfidf_fallback_embed(self, texts: List[str]) -> np.ndarray:
        """Lightweight offline fallback embedding generator."""
        embeddings = []
        for text in texts:
            words = text.lower().split()
            vector = np.zeros(384, dtype=np.float32)
            for word in words:
                hash_val = sum(ord(c) for c in word) % 384
                vector[hash_val] += 1.0
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            embeddings.append(vector)
        return np.array(embeddings, dtype=np.float32)


embedder = MultilingualEmbedder()
