"""
Document loader & chunker for the ASTRAIOS RAG pipeline.

Reads .txt and .pdf files from a given directory and returns a list of
text chunks (with source metadata) using llama-index utilities.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

from ingestion.config import CHUNK_SIZE, CHUNK_OVERLAP, SUPPORTED_EXTENSIONS


@dataclass
class TextChunk:
    """A single chunk of text with source metadata."""
    text: str
    source_file: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


def load_and_chunk_documents(
    data_dir: str | Path,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[TextChunk]:
    """
    Load documents from *data_dir* and split them into chunks.

    Parameters
    ----------
    data_dir : str | Path
        Path to the folder containing raw documents (.txt, .pdf).
    chunk_size : int
        Maximum number of tokens per chunk (default from config).
    chunk_overlap : int
        Number of overlapping tokens between consecutive chunks
        (default from config).

    Returns
    -------
    List[TextChunk]
        Ordered list of text chunks with source metadata.
    """
    data_dir = Path(data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    # Collect files with supported extensions
    input_files: list[Path] = []
    for ext in SUPPORTED_EXTENSIONS:
        input_files.extend(data_dir.glob(f"*{ext}"))

    if not input_files:
        raise ValueError(
            f"No supported files ({SUPPORTED_EXTENSIONS}) found in {data_dir}"
        )

    # Use llama-index SimpleDirectoryReader to load documents
    reader = SimpleDirectoryReader(input_files=[str(f) for f in input_files])
    documents = reader.load_data()

    # Split documents into chunks using SentenceSplitter
    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    nodes = splitter.get_nodes_from_documents(documents)

    # Convert to our lightweight TextChunk dataclass
    chunks: List[TextChunk] = []
    for idx, node in enumerate(nodes):
        source_file = node.metadata.get(
            "file_name",
            node.metadata.get("file_path", "unknown"),
        )
        chunks.append(
            TextChunk(
                text=node.get_content(),
                source_file=source_file,
                chunk_index=idx,
                metadata=node.metadata,
            )
        )

    return chunks
