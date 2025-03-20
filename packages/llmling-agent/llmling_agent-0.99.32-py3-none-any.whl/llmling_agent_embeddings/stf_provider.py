"""Module providing StreamingTransformer embedding generation."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from llmling_agent.embeddings import EmbeddingProvider


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    import numpy as np


class SentenceTransformerEmbeddings(EmbeddingProvider):
    """Local embeddings using sentence-transformers."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)
        self.dimensions: int = self.model.get_sentence_embedding_dimension()

    async def embed_stream(
        self,
        texts: AsyncIterator[str],
        batch_size: int = 8,
    ) -> AsyncIterator[np.ndarray]:
        batch: list[str] = []

        async for text in texts:
            batch.append(text)
            if len(batch) >= batch_size:
                # Run CPU-intensive encoding in thread pool
                embeddings = await asyncio.to_thread(self.model.encode, batch)
                for embedding in embeddings:  # Convert from numpy
                    yield embedding
                batch = []

        if batch:
            embeddings = await asyncio.to_thread(self.model.encode, batch)
            for embedding in embeddings:
                yield embedding
