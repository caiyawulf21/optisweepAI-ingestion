"""Azure OpenAI / Foundry implementation of EmbeddingProvider.

Pure adapter over shared_pipeline_stages.stage_6_5.embedder.AzureOpenAIEmbedder
— that class already resolves AZURE_EMBEDDINGS_* env vars (falling back to
AZURE_OPENAI_*), batches requests, and is Foundry-endpoint-aware. No new
HTTP code belongs here.
"""

from __future__ import annotations

from providers.embeddings import EmbeddingProvider
from shared_pipeline_stages.stage_6_5.embedder import AzureOpenAIEmbedder


class AzureOpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, embedder: AzureOpenAIEmbedder | None = None) -> None:
        self._embedder = embedder or AzureOpenAIEmbedder()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return self._embedder.embed_texts(texts)

    def embedding_model_id(self) -> str:
        return self._embedder.model_name
