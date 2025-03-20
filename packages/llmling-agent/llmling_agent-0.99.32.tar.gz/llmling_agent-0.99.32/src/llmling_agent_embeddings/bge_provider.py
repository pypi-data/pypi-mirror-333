"""Module providing BGE embedding generation."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, ClassVar

from llmling_agent.embeddings import EmbeddingProvider


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    import numpy as np


class BGEEmbeddings(EmbeddingProvider):
    """Local embeddings using BGE models."""

    dimensions: ClassVar[int] = 1536  # OpenAI-compatible

    def __init__(
        self,
        model_name: str = "BAAI/bge-large-en-v1.5",
    ) -> None:
        from FlagEmbedding import FlagModel

        self.model = FlagModel(model_name, use_fp16=True)  # Half precision

    async def embed_stream(
        self,
        texts: AsyncIterator[str],
        batch_size: int = 8,
    ) -> AsyncIterator[np.ndarray]:
        batch: list[str] = []

        async for text in texts:
            batch.append(text)
            if len(batch) >= batch_size:
                embeddings = await asyncio.to_thread(self.model.encode, batch)
                for embedding in embeddings:
                    yield embedding
                batch = []

        if batch:
            embeddings = await asyncio.to_thread(self.model.encode, batch)
            for embedding in embeddings:
                yield embedding
