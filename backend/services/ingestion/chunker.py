"""
Semantic Chunker — Phase D of Source Intelligence Layer.

Chunks text for RAG retrieval using a paragraph-aware sliding window strategy.
Target: 400-600 tokens per chunk, 50 token overlap.
"""

import logging
from typing import List

logger = logging.getLogger(__name__)


class SemanticChunker:
    """
    Chunks text for RAG retrieval.
    Strategy: paragraph-aware sliding window.
    Target: 400-600 tokens per chunk, 50 token overlap.
    """

    CHUNK_TARGET_TOKENS = 500
    OVERLAP_TOKENS = 50

    def __init__(self):
        try:
            import tiktoken
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            logger.warning("tiktoken not installed, using approximate token counting")
            self.tokenizer = None

    def chunk(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split text into overlapping chunks.

        Args:
            text: The full text to chunk.
            metadata: Optional metadata dict to merge into each chunk.

        Returns:
            List of chunk dicts with keys: text, token_count, chunk_index, metadata
        """
        if not text or not text.strip():
            return []

        metadata = metadata or {}

        # Split by double newline (paragraph boundaries)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        if not paragraphs:
            # Fallback: split by single newline
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

        if not paragraphs:
            return []

        chunks = []
        current_chunk_texts = []
        current_token_count = 0
        chunk_index = 0

        for para in paragraphs:
            para_tokens = self._count_tokens(para)

            # If a single paragraph exceeds target, split it
            if para_tokens > self.CHUNK_TARGET_TOKENS * 1.5:
                # Flush current chunk first
                if current_chunk_texts:
                    chunks.append(self._make_chunk(
                        current_chunk_texts, chunk_index, metadata
                    ))
                    chunk_index += 1
                    # Keep overlap from current chunk
                    overlap_text = self._get_overlap_text(current_chunk_texts)
                    current_chunk_texts = [overlap_text] if overlap_text else []
                    current_token_count = self._count_tokens(overlap_text) if overlap_text else 0

                # Split the large paragraph into sentence-level chunks
                sub_chunks = self._split_large_paragraph(para, para_tokens)
                for sub in sub_chunks:
                    chunks.append(self._make_chunk(
                        [sub], chunk_index, metadata
                    ))
                    chunk_index += 1
                continue

            # If adding this paragraph exceeds target, save chunk and start new one
            if current_token_count + para_tokens > self.CHUNK_TARGET_TOKENS and current_chunk_texts:
                chunks.append(self._make_chunk(
                    current_chunk_texts, chunk_index, metadata
                ))
                chunk_index += 1
                # Keep overlap from current chunk
                overlap_text = self._get_overlap_text(current_chunk_texts)
                current_chunk_texts = [overlap_text] if overlap_text else []
                current_token_count = self._count_tokens(overlap_text) if overlap_text else 0

            current_chunk_texts.append(para)
            current_token_count += para_tokens

        # Flush remaining
        if current_chunk_texts:
            chunks.append(self._make_chunk(
                current_chunk_texts, chunk_index, metadata
            ))

        return chunks

    def _make_chunk(self, texts: List[str], index: int, metadata: dict) -> dict:
        """Create a chunk dict from a list of text segments."""
        text = "\n\n".join(texts)
        return {
            "text": text,
            "token_count": self._count_tokens(text),
            "chunk_index": index,
            "metadata": dict(metadata),
        }

    def _get_overlap_text(self, texts: List[str]) -> str:
        """
        Extract the last OVERLAP_TOKENS worth of text from a list of segments.
        """
        if not texts:
            return ""

        full = "\n\n".join(texts)
        tokens = self._tokenize(full)

        if len(tokens) <= self.OVERLAP_TOKENS:
            return full

        overlap_tokens = tokens[-self.OVERLAP_TOKENS:]
        return self._detokenize(overlap_tokens)

    def _split_large_paragraph(self, paragraph: str, token_count: int) -> List[str]:
        """Split a very large paragraph into smaller chunks."""
        # Split by sentence boundaries
        import re
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 1:
            # Fallback: split by character count
            words = paragraph.split()
            mid = len(words) // 2
            return [" ".join(words[:mid]), " ".join(words[mid:])]

        chunks = []
        current = []
        current_tokens = 0

        for sentence in sentences:
            sent_tokens = self._count_tokens(sentence)
            if current_tokens + sent_tokens > self.CHUNK_TARGET_TOKENS and current:
                chunks.append(" ".join(current))
                current = []
                current_tokens = 0
            current.append(sentence)
            current_tokens += sent_tokens

        if current:
            chunks.append(" ".join(current))

        return chunks if chunks else [paragraph]

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken or approximate method."""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        # Approximate: 1 token ≈ 4 characters for English text
        return max(1, len(text) // 4)

    def _tokenize(self, text: str) -> List[int]:
        """Tokenize text to token IDs."""
        if self.tokenizer:
            return self.tokenizer.encode(text)
        # Fallback: character-level (not ideal but functional)
        return [ord(c) for c in text]

    def _detokenize(self, tokens: List[int]) -> str:
        """Convert token IDs back to text."""
        if self.tokenizer:
            return self.tokenizer.decode(tokens)
        return "".join(chr(t) for t in tokens if t < 128)