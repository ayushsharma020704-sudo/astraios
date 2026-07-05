"""
test_pipeline.py — End-to-end local test for the ASTRAIOS RAG pipeline.

This script:
  1. Loads sample .txt files from data/raw/
  2. Chunks them using the ingestion module
  3. Generates embeddings with sentence-transformers
  4. Builds a small in-memory FAISS index
  5. Saves the index + chunk metadata to a temp directory
  6. Instantiates the Retriever and runs a sample query
  7. Prints the top results to prove retrieval works
"""

from __future__ import annotations

import pickle
import shutil
import tempfile
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ── Add the rag-pipeline root to sys.path so imports resolve ──
import sys

PIPELINE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE_ROOT))

from ingestion.config import EMBEDDING_MODEL_NAME
from ingestion.loader import load_and_chunk_documents
from query.retriever import Retriever


def main() -> None:
    data_dir = PIPELINE_ROOT / "data" / "raw"
    print(f"[DIR]  Loading documents from: {data_dir}\n")

    # -- Step 1: Load & Chunk ------------------------------------------
    chunks = load_and_chunk_documents(data_dir)
    print(f"[OK]  Loaded {len(chunks)} chunks from {len(set(c.source_file for c in chunks))} files\n")

    for i, chunk in enumerate(chunks):
        preview = chunk.text[:80].replace("\n", " ")
        print(f"   [{i:02d}] {chunk.source_file:<25s}  {preview}...")
    print()

    # -- Step 2: Generate Embeddings -----------------------------------
    print(f"[MODEL]  Loading embedding model: {EMBEDDING_MODEL_NAME}")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    texts = [c.text for c in chunks]
    print(f"[EMB]  Generating embeddings for {len(texts)} chunks ...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    embeddings = np.array(embeddings, dtype=np.float32)
    print(f"[OK]  Embeddings shape: {embeddings.shape}\n")

    # -- Step 3: Build FAISS Index -------------------------------------
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner-product (cosine) on normalized vecs
    index.add(embeddings)
    print(f"[IDX]  FAISS index built -- {index.ntotal} vectors, dim={dimension}\n")

    # -- Step 4: Save Index + Metadata ---------------------------------
    tmp_dir = Path(tempfile.mkdtemp(prefix="astraios_rag_"))
    faiss.write_index(index, str(tmp_dir / "index.faiss"))

    chunk_meta = [
        {
            "text": c.text,
            "source_file": c.source_file,
            "chunk_index": c.chunk_index,
        }
        for c in chunks
    ]
    with open(tmp_dir / "chunks.pkl", "wb") as f:
        pickle.dump(chunk_meta, f)

    print(f"[SAVE]  Index saved to: {tmp_dir}\n")

    # -- Step 5: Query -------------------------------------------------
    retriever = Retriever(index_path=tmp_dir)

    queries = [
        "What is the Big Bang theory and when did it happen?",
        "Tell me about the James Webb Space Telescope",
        "Where is our Solar System located in the Milky Way?",
    ]

    for query_text in queries:
        print(f"[QUERY]  \"{query_text}\"")
        results = retriever.query(query_text, top_k=3)
        for rank, r in enumerate(results, 1):
            snippet = r.text[:120].replace("\n", " ")
            print(f"   #{rank}  [score={r.score:.4f}]  {r.source_file}")
            print(f"        {snippet}...")
        print()

    # -- Cleanup -------------------------------------------------------
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print("[DONE]  Test complete -- temporary index cleaned up.")


if __name__ == "__main__":
    main()
