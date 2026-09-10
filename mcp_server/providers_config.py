"""Provider selection via env vars (API-neutral doc Step 2):
OPTISWEEP_LLM_PROVIDER / OPTISWEEP_VISION_PROVIDER /
OPTISWEEP_EMBEDDING_PROVIDER / OPTISWEEP_STORAGE_BACKEND. Shared by both
mcp_server/ and http_server/ (2026-09-09) -- provider selection is
transport-neutral, so this module lives with the original MCP server
rather than being duplicated per transport. Only the providers actually
built in this pass are wired here -- azure/local are the only real
options; anything else raises rather than silently falling back, so a
typo in the env var is caught at startup, not at the first call.
"""

from __future__ import annotations

import os

from providers.embeddings import EmbeddingProvider
from providers.llm import LLMProvider
from providers.storage import StorageProvider
from providers.vision import VisionProvider


def get_llm_provider() -> LLMProvider:
    choice = os.getenv("OPTISWEEP_LLM_PROVIDER", "azure_openai").strip().lower()
    if choice == "azure_openai":
        from providers.azure_openai_llm import AzureOpenAILLMProvider

        return AzureOpenAILLMProvider()
    raise ValueError(f"Unknown OPTISWEEP_LLM_PROVIDER: {choice!r} (only 'azure_openai' is implemented)")


def get_vision_provider() -> VisionProvider:
    choice = os.getenv("OPTISWEEP_VISION_PROVIDER", "azure_cv").strip().lower()
    if choice == "azure_cv":
        from providers.azure_cv_vision import AzureCVVisionProvider

        return AzureCVVisionProvider()
    raise ValueError(f"Unknown OPTISWEEP_VISION_PROVIDER: {choice!r} (only 'azure_cv' is implemented)")


def get_embedding_provider() -> EmbeddingProvider:
    choice = os.getenv("OPTISWEEP_EMBEDDING_PROVIDER", "azure_openai").strip().lower()
    if choice == "azure_openai":
        from providers.azure_openai_embeddings import AzureOpenAIEmbeddingProvider

        return AzureOpenAIEmbeddingProvider()
    raise ValueError(f"Unknown OPTISWEEP_EMBEDDING_PROVIDER: {choice!r} (only 'azure_openai' is implemented)")


def get_storage_provider() -> StorageProvider:
    choice = os.getenv("OPTISWEEP_STORAGE_BACKEND", "local").strip().lower()
    if choice == "local":
        from providers.local_storage import LocalStorageProvider

        return LocalStorageProvider()
    if choice == "azure":
        from providers.azure_storage import AzureStorageProvider

        return AzureStorageProvider()
    raise ValueError(f"Unknown OPTISWEEP_STORAGE_BACKEND: {choice!r} (must be 'local' or 'azure')")
