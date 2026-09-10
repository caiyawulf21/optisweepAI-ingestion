"""Smoke tests through the real FastAPI app + TestClient -- confirms
routing, request/response validation, and status-code mapping actually
work end-to-end, not just the handler functions in isolation
(test_routes.py covers those in depth with real business-logic
assertions; this file is deliberately thin)."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from brain.schemas.review import BrainReview, ReviewKind
from brain_service.tests.conftest import make_entity
from providers.local_storage import LocalStorageProvider

from http_server.app import app


class _NullEmbeddingProvider:
    def embed_texts(self, texts):
        return [[0.0] for _ in texts]

    def embedding_model_id(self):
        return "fake"


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    storage = LocalStorageProvider(root=tmp_path)
    # Provider singletons (2026-09-10) are cached in module-level globals
    # that persist across tests in the same process -- reset them here so
    # each test's own tmp_path-scoped storage is actually what the app
    # uses, not whatever a PRIOR test's singleton already cached.
    monkeypatch.setattr("http_server.app._storage_singleton", None)
    monkeypatch.setattr("http_server.app._embeddings_singleton", None)
    monkeypatch.setattr("http_server.app._llm_singleton", None)
    monkeypatch.setattr("http_server.app.get_storage_provider", lambda: storage)
    monkeypatch.setattr("http_server.app.get_embedding_provider", lambda: _NullEmbeddingProvider())
    return TestClient(app)


def test_context_retrieve_endpoint_returns_200(client: TestClient) -> None:
    response = client.post("/brain/v1/context/retrieve", json={"query_text": "test"})
    assert response.status_code == 200
    body = response.json()
    assert "excerpts" in body
    assert "excerpt_count" in body


def test_troubleshoot_endpoint_returns_200(client: TestClient) -> None:
    response = client.post(
        "/brain/v1/context/troubleshoot",
        json={"session_id": "s1", "observed_signals": ["signal one"]},
    )
    assert response.status_code == 200


def test_list_reviews_endpoint_returns_200_and_open_count(client: TestClient, tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records(
        [
            BrainReview(
                id="review:gap:one", kind=ReviewKind.GAP, affected_record_ids=["entity:system:x"],
                proposed_change="x", status="open",
            )
        ],
        scope="reviews/test",
    )
    response = client.get("/brain/v1/reviews")
    assert response.status_code == 200
    assert response.json()["open_count"] == 1


def test_resolve_review_endpoint_returns_404_for_unknown_review(client: TestClient) -> None:
    response = client.post("/brain/v1/reviews/review:does:not_exist/resolve", json={})
    assert response.status_code == 404


def test_resolve_review_endpoint_returns_400_for_bad_resolution_value(client: TestClient, tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records(
        [
            BrainReview(
                id="review:gap:one", kind=ReviewKind.GAP, affected_record_ids=["entity:system:x"],
                proposed_change="x", status="open",
            )
        ],
        scope="reviews/test",
    )
    response = client.post(
        "/brain/v1/reviews/review:gap:one/resolve", json={"resolution": "not_a_real_resolution"}
    )
    assert response.status_code == 400


def test_context_retrieve_rejects_unknown_fields(client: TestClient) -> None:
    response = client.post(
        "/brain/v1/context/retrieve", json={"query_text": "test", "unexpected_field": "x"}
    )
    assert response.status_code == 422
