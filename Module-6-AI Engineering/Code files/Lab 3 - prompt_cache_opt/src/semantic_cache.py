import time
import numpy as np
from typing import Optional, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.88):
        self.threshold = similarity_threshold
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        # In-memory storage for cached entries: list of dicts with text, embedding, response
        self.cache_entries = []
        self.stats = {"hits": 0, "misses": 0}

    def _cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Calculate cosine similarity between two 1D vectors."""
        dot = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        return float(dot / (norm_a * norm_b)) if norm_a and norm_b else 0.0

    def query(self, user_query: str) -> Tuple[Optional[str], float, bool]:
        """Check cache for a semantically equivalent query. Returns (response, similarity, is_hit)."""
        if not self.cache_entries:
            self.stats["misses"] += 1
            return None, 0.0, False

        query_emb = self.model.encode(user_query)
        best_similarity = -1.0
        matched_response = None

        for entry in self.cache_entries:
            sim = self._cosine_similarity(query_emb, entry["embedding"])
            if sim > best_similarity:
                best_similarity = sim
                matched_response = entry["response"]

        if best_similarity >= self.threshold:
            self.stats["hits"] += 1
            return matched_response, best_similarity, True

        self.stats["misses"] += 1
        return None, best_similarity, False

    def store(self, user_query: str, response: str) -> None:
        """Embed query and store in the cache."""
        query_emb = self.model.encode(user_query)
        self.cache_entries.append({
            "query": user_query,
            "embedding": query_emb,
            "response": response
        })

    def get_hit_ratio(self) -> float:
        """Return the percentage of queries successfully served from cache."""
        total = self.stats["hits"] + self.stats["misses"]
        return round((self.stats["hits"] / total * 100), 2) if total > 0 else 0.0