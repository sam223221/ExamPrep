"""Local sentence-transformers embedder (offline). bge models want a query prefix.

Identical to cyper's ``embedder.py``: ``BAAI/bge-small-en-v1.5`` via
sentence-transformers, the bge query prefix, and ``normalize_embeddings=True`` so
cosine similarity in Chroma is just a dot product. The model is baked into the
Docker image and run with ``HF_HUB_OFFLINE=1`` / ``TRANSFORMERS_OFFLINE=1``.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class Embedder:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_docs(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(QUERY_PREFIX + text, normalize_embeddings=True).tolist()
