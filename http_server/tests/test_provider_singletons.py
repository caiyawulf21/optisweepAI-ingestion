"""Confirms the 2026-09-10 provider-singleton fix actually holds: the real
bug was get_storage_provider()/get_embedding_provider() constructing a
brand-new instance per request, so AzureStorageProvider's own embeddings
cache never warmed up across requests -- every call, not just the first,
paid the full ~210-235s Cosmos scan. These tests assert the singleton
behavior directly, not just that the endpoints still return 200."""

from __future__ import annotations

import threading

import pytest

import http_server.app as app_module


@pytest.fixture(autouse=True)
def _reset_singletons(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(app_module, "_storage_singleton", None)
    monkeypatch.setattr(app_module, "_embeddings_singleton", None)
    monkeypatch.setattr(app_module, "_llm_singleton", None)


def test_get_storage_returns_the_same_instance_across_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    constructed = []

    def _fake_factory():
        instance = object()
        constructed.append(instance)
        return instance

    monkeypatch.setattr(app_module, "get_storage_provider", _fake_factory)

    first = app_module._get_storage()
    second = app_module._get_storage()

    assert first is second
    assert len(constructed) == 1  # the factory ran exactly once, not once per call


def test_get_embeddings_returns_the_same_instance_across_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    constructed = []

    def _fake_factory():
        instance = object()
        constructed.append(instance)
        return instance

    monkeypatch.setattr(app_module, "get_embedding_provider", _fake_factory)

    first = app_module._get_embeddings()
    second = app_module._get_embeddings()

    assert first is second
    assert len(constructed) == 1


def test_get_llm_returns_the_same_instance_across_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    constructed = []

    def _fake_factory():
        instance = object()
        constructed.append(instance)
        return instance

    monkeypatch.setattr(app_module, "get_llm_provider", _fake_factory)

    first = app_module._get_llm()
    second = app_module._get_llm()

    assert first is second
    assert len(constructed) == 1


def test_concurrent_first_calls_construct_only_once(monkeypatch: pytest.MonkeyPatch) -> None:
    """The real deployed app runs sync route handlers in a thread pool --
    two requests racing to be the FIRST cold call must not each construct
    (and one discard) their own provider instance."""
    constructed = []
    construction_started = threading.Event()
    release_construction = threading.Event()

    def _slow_factory():
        constructed.append(object())
        construction_started.set()
        release_construction.wait(timeout=5)
        return constructed[-1]

    monkeypatch.setattr(app_module, "get_storage_provider", _slow_factory)

    results: list[object] = []

    def _call():
        results.append(app_module._get_storage())

    threads = [threading.Thread(target=_call) for _ in range(5)]
    for t in threads:
        t.start()
    construction_started.wait(timeout=5)
    release_construction.set()
    for t in threads:
        t.join(timeout=5)

    assert len(constructed) == 1  # only one thread actually ran the factory
    assert len(set(id(r) for r in results)) == 1  # every thread got the same instance
