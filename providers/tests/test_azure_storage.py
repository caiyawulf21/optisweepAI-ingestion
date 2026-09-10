from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from brain.schemas.common import RecordType
from brain.schemas.entity import Entity, EntityType
from providers.azure_cosmos_config import BrainCosmosSettings
from providers.azure_storage import AzureCosmosStorageError, AzureStorageProvider, _strip_cosmos_fields


def _fake_settings() -> BrainCosmosSettings:
    return BrainCosmosSettings(
        endpoint="https://fake.documents.azure.com:443/",
        key="ZmFrZWtleQ==",  # base64("fakekey")
        database="fake_db",
        containers={"brain_entities": "brain_entities", "brain_ingestion_runs": "brain_ingestion_runs"},
    )


def test_missing_settings_raises_runtime_error() -> None:
    incomplete = BrainCosmosSettings(endpoint="", key="", database="", containers={})
    with pytest.raises(RuntimeError, match="not configured"):
        AzureStorageProvider(settings=incomplete)


def test_strip_cosmos_fields_removes_system_and_partition_key_fields() -> None:
    raw = {"id": "entity:system:x", "name": "X", "_rid": "abc", "_self": "def", "_etag": "ghi", "_ts": 1, "_partition_key": "system"}
    cleaned = _strip_cosmos_fields(raw)
    assert cleaned == {"id": "entity:system:x", "name": "X"}


def test_document_id_rejects_forbidden_characters() -> None:
    provider = AzureStorageProvider(settings=_fake_settings())
    entity = Entity(
        id="entity/system:x", entity_type=EntityType.SYSTEM, name="X", description="y",
        source_refs=["evidence:test:seed"],
    )
    with pytest.raises(AzureCosmosStorageError, match="forbidden"):
        provider._document_id(entity)


class _FakeHTTPResponse:
    def __init__(self, payload: dict, headers: dict | None = None) -> None:
        self._payload = payload
        self.headers = headers or {}

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_save_brain_records_writes_partition_key_field() -> None:
    provider = AzureStorageProvider(settings=_fake_settings())
    entity = Entity(
        id="entity:system:x", entity_type=EntityType.SYSTEM, name="X", description="y",
        source_refs=["evidence:test:seed"],
    )

    captured = {}

    def fake_urlopen(request, timeout=None):
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["headers"] = dict(request.header_items())
        return _FakeHTTPResponse({})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        provider.save_brain_records([entity], scope="operational_sources/test")

    assert captured["body"]["_partition_key"] == "system"
    assert captured["body"]["id"] == "entity:system:x"
    assert any(k.lower() == "x-ms-documentdb-is-upsert" for k in captured["headers"])


def test_query_container_strips_cosmos_fields_before_validating() -> None:
    provider = AzureStorageProvider(settings=_fake_settings())
    raw_doc = {
        "id": "entity:system:x",
        "type": "entity",
        "schema_version": "1.0",
        "source_refs": ["evidence:test:seed"],
        "constraints": {"sites": [], "product_versions": [], "environments": []},
        "validation_status": "operational_unreviewed",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "entity_type": "system",
        "name": "X",
        "description": "y",
        "aliases": [],
        "payload": {},
        "_rid": "fake",
        "_self": "fake",
        "_etag": "fake",
        "_ts": 1,
        "_partition_key": "system",
    }

    def fake_urlopen(request, timeout=None):
        return _FakeHTTPResponse({"Documents": [raw_doc]}, headers={})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        results = provider._query_container("brain_entities", RecordType.ENTITY)

    assert len(results) == 1
    assert results[0].id == "entity:system:x"


def test_get_document_returns_none_on_404() -> None:
    import urllib.error

    provider = AzureStorageProvider(settings=_fake_settings())

    def fake_urlopen(request, timeout=None):
        raise urllib.error.HTTPError(request.full_url, 404, "not found", {}, None)

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        result = provider._get_document(container="brain_ingestion_runs", document_id="missing", partition_key="missing")

    assert result is None


def test_upsert_raises_azure_cosmos_storage_error_on_http_error() -> None:
    import io
    import urllib.error

    provider = AzureStorageProvider(settings=_fake_settings())

    def fake_urlopen(request, timeout=None):
        raise urllib.error.HTTPError(request.full_url, 400, "bad request", {}, io.BytesIO(b"bad body"))

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        with pytest.raises(AzureCosmosStorageError, match="400"):
            provider._upsert_document(container="brain_entities", document={"id": "x"}, partition_key="x")


def _fake_settings_with_embeddings() -> BrainCosmosSettings:
    return BrainCosmosSettings(
        endpoint="https://fake.documents.azure.com:443/",
        key="ZmFrZWtleQ==",
        database="fake_db",
        containers={"brain_embeddings": "brain_embeddings"},
    )


def test_save_embeddings_writes_partition_key_from_record_type() -> None:
    provider = AzureStorageProvider(settings=_fake_settings_with_embeddings())
    captured = {}

    def fake_urlopen(request, timeout=None):
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return _FakeHTTPResponse({})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        provider.save_embeddings(
            [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1]}]
        )

    assert captured["body"]["_partition_key"] == "entity"
    assert captured["body"]["id"] == "entity:system:a"


def test_load_all_embeddings_strips_cosmos_fields() -> None:
    provider = AzureStorageProvider(settings=_fake_settings_with_embeddings())
    raw_doc = {
        "record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1],
        "id": "entity:system:a", "_rid": "x", "_self": "x", "_etag": "x", "_ts": 1, "_partition_key": "entity",
    }

    def fake_urlopen(request, timeout=None):
        return _FakeHTTPResponse({"Documents": [raw_doc]}, headers={})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        results = provider.load_all_embeddings()

    assert results == [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1], "id": "entity:system:a"}]


def _entity_doc() -> dict:
    return {
        "id": "entity:system:x", "type": "entity", "schema_version": "1.0",
        "source_refs": ["evidence:test:seed"],
        "constraints": {"sites": [], "product_versions": [], "environments": []},
        "validation_status": "operational_unreviewed",
        "created_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:00:00Z",
        "entity_type": "system", "name": "X", "description": "y", "aliases": [], "payload": {},
        "_rid": "fake", "_self": "fake", "_etag": "fake", "_ts": 1, "_partition_key": "system",
    }


def test_query_container_caches_after_first_call() -> None:
    """The real production bottleneck (2026-09-10): every call to
    load_brain_context/load_brain_records previously re-fetched the ENTIRE
    container from Cosmos with no caching at all, unlike load_all_embeddings.
    A second _query_container call for the same record type must not hit
    the network again."""
    provider = AzureStorageProvider(settings=_fake_settings())
    call_count = {"n": 0}

    def fake_urlopen(request, timeout=None):
        call_count["n"] += 1
        return _FakeHTTPResponse({"Documents": [_entity_doc()]}, headers={})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_urlopen):
        first = provider._query_container("brain_entities", RecordType.ENTITY)
        second = provider._query_container("brain_entities", RecordType.ENTITY)

    assert call_count["n"] == 1  # only the first call hit the network
    assert first == second


def test_save_brain_records_invalidates_only_the_written_record_type() -> None:
    provider = AzureStorageProvider(
        settings=BrainCosmosSettings(
            endpoint="https://fake.documents.azure.com:443/", key="ZmFrZWtleQ==", database="fake_db",
            containers={"brain_entities": "brain_entities", "brain_capabilities": "brain_capabilities"},
        )
    )
    call_count = {"entity": 0}

    def fake_query_urlopen(request, timeout=None):
        call_count["entity"] += 1
        return _FakeHTTPResponse({"Documents": [_entity_doc()]}, headers={})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_query_urlopen):
        provider._query_container("brain_entities", RecordType.ENTITY)  # warm the cache
    assert call_count["entity"] == 1

    # Write a DIFFERENT record type (Capability) -- must not invalidate the
    # already-cached Entity scan.
    from brain.schemas.capability import Capability, CapabilityKind

    capability = Capability(
        id="capability:x", name="x", capability_kind=CapabilityKind.DIAGNOSTIC,
        source_refs=["evidence:test:seed"],
    )

    def fake_write_urlopen(request, timeout=None):
        return _FakeHTTPResponse({})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_write_urlopen):
        provider.save_brain_records([capability], scope="ontology_catalogs")

    with patch("providers.azure_storage.urllib.request.urlopen", fake_query_urlopen):
        provider._query_container("brain_entities", RecordType.ENTITY)  # should still be cached

    assert call_count["entity"] == 1  # no second network call for entities


def test_save_brain_records_invalidates_the_written_record_type() -> None:
    provider = AzureStorageProvider(settings=_fake_settings())
    call_count = {"n": 0}

    def fake_query_urlopen(request, timeout=None):
        call_count["n"] += 1
        return _FakeHTTPResponse({"Documents": [_entity_doc()]}, headers={})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_query_urlopen):
        provider._query_container("brain_entities", RecordType.ENTITY)  # warm the cache
    assert call_count["n"] == 1

    entity = Entity(
        id="entity:system:x", entity_type=EntityType.SYSTEM, name="X", description="y",
        source_refs=["evidence:test:seed"],
    )

    def fake_write_urlopen(request, timeout=None):
        return _FakeHTTPResponse({})

    with patch("providers.azure_storage.urllib.request.urlopen", fake_write_urlopen):
        provider.save_brain_records([entity], scope="operational_sources/test")  # writes an Entity

    with patch("providers.azure_storage.urllib.request.urlopen", fake_query_urlopen):
        provider._query_container("brain_entities", RecordType.ENTITY)  # must re-fetch, not use stale cache

    assert call_count["n"] == 2  # a second network call happened after the invalidating write
