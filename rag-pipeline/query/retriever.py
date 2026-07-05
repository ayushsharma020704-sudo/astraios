"""
Retriever for the ASTRAIOS RAG pipeline.

Loads a saved FAISS index (and its associated chunk metadata) and performs
similarity search against a query string, returning the top-k most relevant
text chunks with their source filenames.
"""

from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from ingestion.config import EMBEDDING_MODEL_NAME


@dataclass
class RetrievalResult:
    """A single retrieval result containing the matched chunk and metadata."""
    text: str
    source_file: str
    score: float
    chunk_index: int


class Retriever:
    """
    Loads a persisted FAISS index and performs similarity search.

    Parameters
    ----------
    index_path : str | Path
        Path to the directory containing the saved FAISS index and metadata.
        Expected files inside:
          - ``index.faiss``   — the FAISS index
          - ``chunks.pkl``    — pickled list of dicts with keys
                                ``text``, ``source_file``, ``chunk_index``
    model_name : str
        Name of the sentence-transformers model used for embedding queries.
    """

    def __init__(
        self,
        index_path: str | Path,
        model_name: str = EMBEDDING_MODEL_NAME,
    ) -> None:
        self.index_path = Path(index_path)
        self.model = SentenceTransformer(model_name)

        # Load FAISS index
        faiss_file = self.index_path / "index.faiss"
        if not faiss_file.exists():
            raise FileNotFoundError(f"FAISS index not found at {faiss_file}")
        self.index = faiss.read_index(str(faiss_file))

        # Load chunk metadata
        chunks_file = self.index_path / "chunks.pkl"
        if not chunks_file.exists():
            raise FileNotFoundError(f"Chunk metadata not found at {chunks_file}")
        with open(chunks_file, "rb") as f:
            self.chunks: List[dict] = pickle.load(f)

    def query(self, text: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Retrieve the top-k most similar chunks for a query string.

        Parameters
        ----------
        text : str
            The natural-language query.
        top_k : int
            Number of results to return (default 5).

        Returns
        -------
        List[RetrievalResult]
            Matched chunks ordered by descending similarity.
        """
        # Embed the query
        query_embedding = self.model.encode([text], normalize_embeddings=True)
        query_embedding = np.array(query_embedding, dtype=np.float32)

        # Search the FAISS index
        distances, indices = self.index.search(query_embedding, top_k)

        results: List[RetrievalResult] = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue  # no more results
            chunk = self.chunks[idx]
            results.append(
                RetrievalResult(
                    text=chunk["text"],
                    source_file=chunk["source_file"],
                    score=float(dist),
                    chunk_index=chunk["chunk_index"],
                )
            )

        return results
