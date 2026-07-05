"""
Configuration constants for the ASTRAIOS RAG ingestion pipeline.
"""

# ── Chunking parameters ──────────────────────────────────────────
CHUNK_SIZE: int = 512          # Maximum tokens per chunk
CHUNK_OVERLAP: int = 50        # Token overlap between consecutive chunks

# ── Embedding model ──────────────────────────────────────────────
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"  # Free, lightweight, from sentence-transformers

# ── Supported file extensions ────────────────────────────────────
SUPPORTED_EXTENSIONS: list[str] = [".txt", ".pdf"]
