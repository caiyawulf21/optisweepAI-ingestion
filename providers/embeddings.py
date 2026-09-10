"""Provider-neutral embedding interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts, returning one vector per input in order."""

    @abstractmethod
    def embedding_model_id(self) -> str:
        """Identifier for the embedding model/deployment in use."""
