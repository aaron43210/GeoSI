# -*- coding: utf-8 -*-
"""
GeoSI RAG — Text Chunker
═══════════════════════════════════════════════════════════════════

Splits documents into overlapping chunks for embedding.

Strategy: Sentence-aware splitting — splits on sentence boundaries
while respecting chunk_size limits and maintaining overlap for
context continuity.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any

from geosi_rag.document_loader import Document

logger = logging.getLogger("geosi_rag.chunker")

# Attempt to load the C++ extension for O(N) chunking
_CPP_CHUNKER_AVAILABLE = False
try:
    from geosi_rag.geosi_chunker import chunk_text as _cpp_chunk_text
    _CPP_CHUNKER_AVAILABLE = True
except ImportError:
    pass


@dataclass
class Chunk:
    """
    A text chunk ready for embedding.

    Attributes:
        text: The chunk text content
        source: Source file path
        chunk_index: Position within the source document
        metadata: Extra metadata (document format, source, etc.)
    """
    text: str
    source: str = ""
    chunk_index: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        preview = self.text[:60].replace("\n", " ")
        return f"Chunk({self.chunk_index}, '{preview}...', {len(self.text)} chars)"

    def __len__(self):
        return len(self.text)


# Sentence boundary patterns
_SENTENCE_ENDINGS = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")


class Chunker:
    """
    Splits documents into overlapping, sentence-aware chunks.

    Usage:
        chunker = Chunker(chunk_size=512, overlap=64)
        chunks = chunker.chunk_document(document)
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        """
        Args:
            chunk_size: Target chunk size in characters.
            overlap: Number of overlapping characters between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, doc: Document) -> List[Chunk]:
        """
        Split a document into overlapping chunks.

        Algorithm:
            1. If C++ extension is loaded, use O(N) chunk_text natively.
            2. Otherwise fallback to Python:
               a. Split text into sentences
               b. Greedily pack sentences into chunks up to chunk_size
               c. On chunk boundary, overlap by including last sentences

        Args:
            doc: Document to chunk.

        Returns:
            List of Chunk objects.
        """
        if not doc.content:
            return []

        if _CPP_CHUNKER_AVAILABLE:
            raw_chunks = _cpp_chunk_text(doc.content, self.chunk_size, self.overlap)
            chunks = [self._make_chunk(txt, doc, i) for i, txt in enumerate(raw_chunks)]
            logger.debug(
                f"[C++] Chunked '{doc.source_path}' → {len(chunks)} chunks "
                f"(avg {sum(len(c) for c in chunks) // max(len(chunks), 1)} chars)"
            )
            return chunks

        sentences = self._split_sentences(doc.content)
        if not sentences:
            return []

        chunks = []
        current_sentences = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            # If a single sentence exceeds chunk_size, force-split it
            if sentence_len > self.chunk_size:
                # Flush current buffer first
                if current_sentences:
                    chunk_text = " ".join(current_sentences)
                    chunks.append(self._make_chunk(
                        chunk_text, doc, len(chunks)
                    ))
                    current_sentences = []
                    current_length = 0

                # Split the long sentence into fixed-size pieces
                for i in range(0, sentence_len, self.chunk_size - self.overlap):
                    piece = sentence[i:i + self.chunk_size]
                    chunks.append(self._make_chunk(piece, doc, len(chunks)))
                continue

            # Check if adding this sentence would exceed chunk_size
            new_length = current_length + sentence_len + (1 if current_sentences else 0)
            if new_length > self.chunk_size and current_sentences:
                # Emit current chunk
                chunk_text = " ".join(current_sentences)
                chunks.append(self._make_chunk(chunk_text, doc, len(chunks)))

                # Determine overlap: keep the last few sentences that fit
                # within the overlap budget
                overlap_sentences = []
                overlap_len = 0
                for s in reversed(current_sentences):
                    if overlap_len + len(s) + 1 > self.overlap:
                        break
                    overlap_sentences.insert(0, s)
                    overlap_len += len(s) + 1

                current_sentences = overlap_sentences
                current_length = overlap_len

            current_sentences.append(sentence)
            current_length += sentence_len + (1 if len(current_sentences) > 1 else 0)

        # Flush remaining sentences
        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(self._make_chunk(chunk_text, doc, len(chunks)))

        logger.debug(
            f"Chunked '{doc.source_path}' → {len(chunks)} chunks "
            f"(avg {sum(len(c) for c in chunks) // max(len(chunks), 1)} chars)"
        )
        return chunks

    def chunk_documents(self, docs: List[Document]) -> List[Chunk]:
        """Chunk multiple documents at once."""
        all_chunks = []
        for doc in docs:
            all_chunks.extend(self.chunk_document(doc))
        logger.info(
            f"Chunked {len(docs)} documents → {len(all_chunks)} total chunks"
        )
        return all_chunks

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences, respecting paragraph breaks.

        Strategy:
            1. Split on paragraph breaks (double newlines)
            2. Within paragraphs, split on sentence boundaries
            3. Clean up whitespace
        """
        # First split on paragraph boundaries
        paragraphs = _PARAGRAPH_BREAK.split(text)

        sentences = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Split paragraph into sentences
            para_sentences = _SENTENCE_ENDINGS.split(para)

            for sent in para_sentences:
                sent = sent.strip()
                if sent:
                    # Collapse internal whitespace
                    sent = re.sub(r"\s+", " ", sent)
                    sentences.append(sent)

        return sentences

    @staticmethod
    def _make_chunk(text: str, doc: Document, index: int) -> Chunk:
        """Create a Chunk from text and document metadata."""
        return Chunk(
            text=text,
            source=doc.source_path,
            chunk_index=index,
            metadata={
                "format": doc.format,
                "filename": doc.metadata.get("filename", ""),
                **{k: v for k, v in doc.metadata.items() if k != "filename"},
            },
        )
