from __future__ import annotations

from unittest.mock import MagicMock

from providers.azure_openai_embeddings import AzureOpenAIEmbeddingProvider


def test_embed_texts_delegates_to_embedder() -> None:
    fake_embedder = MagicMock()
    fake_embedder.embed_texts.return_value = [[0.1, 0.2], [0.3, 0.4]]
    provider = AzureOpenAIEmbeddingProvider(embedder=fake_embedder)

    result = provider.embed_texts(["hello", "world"])

    fake_embedder.embed_texts.assert_called_once_with(["hello", "world"])
    assert result == [[0.1, 0.2], [0.3, 0.4]]


def test_embedding_model_id_returns_embedder_model_name() -> None:
    fake_embedder = MagicMock()
    fake_embedder.model_name = "text-embedding-3-small"
    provider = AzureOpenAIEmbeddingProvider(embedder=fake_embedder)

    assert provider.embedding_model_id() == "text-embedding-3-small"
