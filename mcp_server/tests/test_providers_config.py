from __future__ import annotations

import pytest

from mcp_server.providers_config import get_storage_provider


def test_get_storage_provider_defaults_to_local(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPTISWEEP_STORAGE_BACKEND", raising=False)
    from providers.local_storage import LocalStorageProvider

    assert isinstance(get_storage_provider(), LocalStorageProvider)


def test_get_storage_provider_resolves_azure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPTISWEEP_STORAGE_BACKEND", "azure")
    monkeypatch.setattr(
        "providers.azure_storage.AzureStorageProvider.__init__", lambda self: None
    )
    from providers.azure_storage import AzureStorageProvider

    assert isinstance(get_storage_provider(), AzureStorageProvider)


def test_get_storage_provider_raises_for_unknown_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPTISWEEP_STORAGE_BACKEND", "not_a_real_backend")
    with pytest.raises(ValueError, match="Unknown OPTISWEEP_STORAGE_BACKEND"):
        get_storage_provider()
