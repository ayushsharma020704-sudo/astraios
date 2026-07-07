"""
Cosmic Historian Tool — calls the real RAG retriever to fetch relevant
astronomical context chunks from the FAISS index.

Falls back to hardcoded context if the FAISS index hasn't been built yet.
"""

from __future__ import annotations

import sys
from pathlib import Path

from crewai.tools import tool

# ---------------------------------------------------------------------------
# Path setup — the rag-pipeline lives alongside the backend dir
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parents[3]           # e:\Projects\astraios
_RAG_PIPELINE = _PROJECT_ROOT / "rag-pipeline"
_INDEX_DIR = _RAG_PIPELINE / "data" / "index"

# Add rag-pipeline to sys.path so we can import its modules
if str(_RAG_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_RAG_PIPELINE))


def _try_rag_query(query: str, top_k: int = 3) -> str | None:
    """Attempt a real RAG retrieval. Returns None on failure."""
    try:
        from query.retriever import Retriever            # type: ignore[import]

        if not (_INDEX_DIR / "index.faiss").exists():
            return None

        retriever = Retriever(index_path=str(_INDEX_DIR))
        results = retriever.query(query, top_k=top_k)
        if not results:
            return None

        parts: list[str] = ["=== RAG Retrieval Results (real) ===\n"]
        for i, r in enumerate(results, 1):
            parts.append(
                f"[{i}] Source: {r.source_file}  |  Score: {r.score:.4f}\n"
                f"    {r.text[:300]}{'…' if len(r.text) > 300 else ''}\n"
            )
        return "\n".join(parts)
    except Exception:
        return None


_FALLBACK = (
    "=== Cosmic History Context (fallback — no FAISS index found) ===\n\n"
    "Historical Context for Exoplanet Missions:\n\n"
    "1. Kepler Space Telescope (2009–2018):\n"
    "   Launched by NASA, Kepler discovered 2,662 confirmed exoplanets using the\n"
    "   transit method. Kepler-452b was announced on July 23, 2015, as the first\n"
    "   near-Earth-size planet in the habitable zone of a Sun-like star.\n\n"
    "2. The Drake Equation & SETI Context:\n"
    "   Frank Drake's 1961 equation estimates communicative civilizations in the\n"
    "   Milky Way. Kepler-452b's Earth Similarity Index of 0.83 makes it a prime\n"
    "   candidate for targeted SETI observations.\n\n"
    "3. Breakthrough Starshot (2016–present):\n"
    "   Yuri Milner's initiative aims to send gram-scale probes to Alpha Centauri\n"
    "   at 0.2c using laser-driven light sails. The same technology could\n"
    "   theoretically be scaled for missions to more distant targets.\n\n"
    "4. James Webb Space Telescope (2021–present):\n"
    "   JWST's NIRSpec and MIRI instruments can characterize exoplanet atmospheres\n"
    "   via transmission spectroscopy, providing data on potential biosignatures\n"
    "   for targets like Kepler-452b."
)


@tool("Cosmic History Archive")
def cosmic_historian_tool(query: str) -> str:
    """Searches the ASTRAIOS cosmic-history knowledge base (RAG) for relevant
    historical context, astronomical discoveries, and past mission data.
    Input should be a natural-language query about the mission or target."""
    result = _try_rag_query(query)
    if result is not None:
        print("\n\n>>> HISTORIAN TOOL: HITTING REAL FAISS INDEX <<<\n")
        return result
    print("\n\n>>> HISTORIAN TOOL: HITTING FALLBACK <<<\n")
    return _FALLBACK
