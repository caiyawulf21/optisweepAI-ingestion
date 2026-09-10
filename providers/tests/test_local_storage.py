from __future__ import annotations

import json
from pathlib import Path

import pytest

from brain.schemas.common import RecordType
from brain.schemas.entity import Entity, EntityType
from brain.schemas.evidence_unit import EvidenceContent, EvidenceKind, EvidenceUnit
from providers.local_storage import LocalStorageProvider


def _entity(entity_id: str = "entity:system:test_system") -> Entity:
    return Entity(
        id=entity_id,
        entity_type=EntityType.SYSTEM,
        name="Test System",
        description="A system used only in tests.",
        source_refs=["evidence:test:seed"],
    )


def _evidence(evidence_id: str = "evidence:test:seed") -> EvidenceUnit:
    return EvidenceUnit(
        id=evidence_id,
        evidence_kind=EvidenceKind.SME_NOTE,
        source_type="test",
        source_id="source:test",
        content=EvidenceContent(text="test evidence", is_verbatim=True, content_hash="sha256:deadbeef"),
    )


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    entity = _entity()
    storage.save_brain_records([entity], scope="operational_sources/test_source")

    loaded = storage.load_brain_records(scope="operational_sources/test_source")
    assert len(loaded) == 1
    assert loaded[0].id == entity.id
    assert isinstance(loaded[0], Entity)


def test_load_brain_records_filters_by_type(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity(), _evidence()], scope="incidents/case_test")

    entities_only = storage.load_brain_records(scope="incidents/case_test", record_type=RecordType.ENTITY)
    assert len(entities_only) == 1
    assert entities_only[0].type == RecordType.ENTITY


def test_save_brain_records_merges_by_id_not_overwrite(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity("entity:system:a")], scope="incidents/case_test")
    storage.save_brain_records([_entity("entity:system:b")], scope="incidents/case_test")

    loaded = storage.load_brain_records(scope="incidents/case_test", record_type=RecordType.ENTITY)
    assert {record.id for record in loaded} == {"entity:system:a", "entity:system:b"}


def test_save_brain_records_replaces_existing_id(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    original = _entity()
    storage.save_brain_records([original], scope="incidents/case_test")

    updated = original.model_copy(update={"description": "Updated description."})
    storage.save_brain_records([updated], scope="incidents/case_test")

    loaded = storage.load_brain_records(scope="incidents/case_test", record_type=RecordType.ENTITY)
    assert len(loaded) == 1
    assert loaded[0].description == "Updated description."


def test_load_brain_context_scans_all_scopes(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity("entity:system:a")], scope="incidents/case_1")
    storage.save_brain_records([_entity("entity:system:b")], scope="operational_sources/manual")

    context = storage.load_brain_context()
    assert {record.id for record in context} == {"entity:system:a", "entity:system:b"}


def test_load_brain_context_filters_by_entity_ids(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity("entity:system:a"), _entity("entity:system:b")], scope="incidents/case_1")

    context = storage.load_brain_context(entity_ids=["entity:system:a"])
    assert [record.id for record in context] == ["entity:system:a"]


def test_load_brain_context_excludes_ingestion_runs_dir(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_ingestion_run({"run_id": "run_1", "status": "ok"})
    storage.save_brain_records([_entity()], scope="incidents/case_1")

    context = storage.load_brain_context()
    assert len(context) == 1


def test_ingestion_run_round_trip(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_ingestion_run({"run_id": "run_42", "status": "in_progress"})

    loaded = storage.load_ingestion_run("run_42")
    assert loaded == {"run_id": "run_42", "status": "in_progress"}


def test_load_ingestion_run_missing_returns_none(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    assert storage.load_ingestion_run("does_not_exist") is None


def test_save_ingestion_run_requires_run_id(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    with pytest.raises(ValueError):
        storage.save_ingestion_run({"status": "no id"})


def test_reads_legacy_new_entities_filename(tmp_path: Path) -> None:
    scope_dir = tmp_path / "incidents" / "case_legacy"
    scope_dir.mkdir(parents=True)
    entity = _entity()
    (scope_dir / "new_entities.json").write_text(
        json.dumps([entity.model_dump(mode="json")]), encoding="utf-8"
    )

    storage = LocalStorageProvider(root=tmp_path)
    loaded = storage.load_brain_records(scope="incidents/case_legacy", record_type=RecordType.ENTITY)
    assert len(loaded) == 1
    assert loaded[0].id == entity.id


def test_writes_canonical_entities_filename_not_legacy(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity()], scope="incidents/case_test")

    assert (tmp_path / "incidents" / "case_test" / "entities.json").exists()
    assert not (tmp_path / "incidents" / "case_test" / "new_entities.json").exists()


def test_save_and_load_embeddings_round_trip(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1, 0.2]}]
    )

    loaded = storage.load_all_embeddings()
    assert len(loaded) == 1
    assert loaded[0]["record_id"] == "entity:system:a"
    assert loaded[0]["vector"] == [0.1, 0.2]


def test_load_all_embeddings_filters_by_record_type(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_embeddings(
        [
            {"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1]},
            {"record_id": "claim:x:y", "record_type": "claim", "embedding_model": "m", "vector": [0.2]},
        ]
    )

    entities_only = storage.load_all_embeddings(record_type=RecordType.ENTITY)
    assert [e["record_id"] for e in entities_only] == ["entity:system:a"]


def test_save_embeddings_upserts_by_record_id(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "v1", "vector": [0.1]}]
    )
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "v2", "vector": [0.9]}]
    )

    loaded = storage.load_all_embeddings()
    assert len(loaded) == 1
    assert loaded[0]["embedding_model"] == "v2"


def test_load_all_embeddings_empty_when_none_saved(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    assert storage.load_all_embeddings() == []


def test_embeddings_dir_excluded_from_scope_scan(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity()], scope="incidents/case_1")
    storage.save_embeddings(
        [{"record_id": "entity:system:test_system", "record_type": "entity", "embedding_model": "m", "vector": [0.1]}]
    )

    context = storage.load_brain_context()
    assert len(context) == 1  # the entity, not anything embeddings/ contributes


def test_load_all_embeddings_caches_after_first_call(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "m", "vector": [0.1]}]
    )

    storage.load_all_embeddings()  # warms the cache

    read_calls = []
    original_read_text = Path.read_text

    def counting_read_text(self, *args, **kwargs):
        read_calls.append(self)
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", counting_read_text)
    storage.load_all_embeddings()  # should hit the cache, not disk

    assert read_calls == []


def test_save_embeddings_invalidates_the_cache(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "v1", "vector": [0.1]}]
    )
    storage.load_all_embeddings()  # warms the cache with v1

    storage.save_embeddings(
        [{"record_id": "entity:system:a", "record_type": "entity", "embedding_model": "v2", "vector": [0.9]}]
    )

    loaded = storage.load_all_embeddings()
    assert loaded[0]["embedding_model"] == "v2"  # not the cached v1


def test_find_scope_for_record_returns_the_actual_owning_scope(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity("entity:system:a")], scope="operational_sources/manual_x")

    assert storage.find_scope_for_record("entity:system:a") == "operational_sources/manual_x"


def test_find_scope_for_record_returns_none_when_not_found(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    assert storage.find_scope_for_record("entity:system:does_not_exist") is None


def test_find_scope_for_record_distinguishes_between_multiple_scopes(tmp_path: Path) -> None:
    storage = LocalStorageProvider(root=tmp_path)
    storage.save_brain_records([_entity("entity:system:a")], scope="incidents/case_1")
    storage.save_brain_records([_entity("entity:system:b")], scope="incidents/case_2")

    assert storage.find_scope_for_record("entity:system:a") == "incidents/case_1"
    assert storage.find_scope_for_record("entity:system:b") == "incidents/case_2"
