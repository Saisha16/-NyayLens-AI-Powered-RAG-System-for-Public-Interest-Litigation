"""Semantic similarity search over constitutional provisions and case laws.

Builds an embedding index using sentence-transformers and FAISS to return
contextually relevant legal references for a given issue summary.
"""

from __future__ import annotations

import numpy as np
import faiss
from typing import List, Dict
from sentence_transformers import SentenceTransformer

from backend.constitutional_db import (
    FUNDAMENTAL_RIGHTS,
    DIRECTIVE_PRINCIPLES,
    ADDITIONAL_PROVISIONS,
    TOPIC_CONSTITUTIONAL_MAPPING,
)


# Module-level singletons
_model: SentenceTransformer | None = None
_index: faiss.IndexFlatIP | None = None
_corpus: List[Dict] | None = None
_embeddings: np.ndarray | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        # Good general-purpose semantic similarity model
        _model = SentenceTransformer("all-mpnet-base-v2")
    return _model


def _build_corpus() -> List[Dict]:
    """Collect constitutional articles, DPSPs, and case laws into a corpus."""
    items: List[Dict] = []

    # Fundamental Rights
    for key, fr in FUNDAMENTAL_RIGHTS.items():
        items.append({
            "id": f"fr_{key}",
            "title": fr.get("title", ""),
            "text": fr.get("text", ""),
            "source": fr.get("article", "Fundamental Right"),
            "category": "Fundamental Right",
        })

    # DPSPs
    for key, dp in DIRECTIVE_PRINCIPLES.items():
        items.append({
            "id": f"dp_{key}",
            "title": dp.get("title", ""),
            "text": dp.get("text", ""),
            "source": dp.get("article", "Directive Principle"),
            "category": "Directive Principle",
        })

    # Additional provisions
    for key, ap in ADDITIONAL_PROVISIONS.items():
        items.append({
            "id": f"ap_{key}",
            "title": ap.get("title", ""),
            "text": ap.get("text", ""),
            "source": ap.get("article", "Constitution"),
            "category": "Constitutional Provision",
        })

    # Case laws from topic mappings
    seen_cases = set()
    for topic, mapping in TOPIC_CONSTITUTIONAL_MAPPING.items():
        for case in mapping.get("key_case_laws", []):
            if case not in seen_cases:
                seen_cases.add(case)
                # Split case title if format "Case Name - detail"
                title = case.split(" - ")[0] if " - " in case else case
                items.append({
                    "id": f"case_{len(seen_cases)}",
                    "title": title,
                    "text": case,
                    "source": "Landmark Case Law",
                    "category": "Case Precedent",
                })

    return items


def _init_index():
    """Initialize corpus and FAISS index once."""
    global _index, _corpus, _embeddings
    if _index is not None:
        return

    _corpus = _build_corpus()
    model = _get_model()
    texts = [item["text"] for item in _corpus]

    # Compute embeddings and normalize for cosine similarity via inner product
    emb = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    _embeddings = emb.astype("float32")

    dim = _embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(_embeddings)


def semantic_search(query: str, top_k: int = 5) -> List[Dict]:
    """Return top-k semantically similar legal references for the query.

    Each result contains: source, title, excerpt, category, similarity.
    """
    if not query or len(query.strip()) == 0:
        return []

    _init_index()
    model = _get_model()

    q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
    scores, idxs = _index.search(q, top_k)
    idxs = idxs[0]
    scores = scores[0]

    results: List[Dict] = []
    for i, score in zip(idxs, scores):
        item = _corpus[i]
        results.append({
            "source": item["source"],
            "title": item["title"],
            "excerpt": item["text"][:400],
            "category": item["category"],
            "similarity": float(score),
        })
    return results
