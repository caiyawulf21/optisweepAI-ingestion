from __future__ import annotations

from pathlib import Path

import pytest

from brain.schemas.capability import SqlFieldNote, SupportContract
from brain_service.tests.conftest import make_capability, make_entity
from providers.local_storage import LocalStorageProvider
from shared_pipeline_stages.brain_ontology_bridge import (
    brain_contracts_for_capabilities,
    brain_snippets_for_stage5_playbook,
)


@pytest.fixture()
def storage(tmp_path: Path) -> LocalStorageProvider:
    return LocalStorageProvider(root=tmp_path)


class FakeEmbeddingProvider:
    """Returns a fixed vector per input text, keyed by substring match, so
    tests can control which stored embeddings look "similar" without a
    real embedding call."""

    def __init__(self, vector_by_keyword: dict[str, list[float]], default: list[float]) -> None:
        self._vector_by_keyword = vector_by_keyword
        self._default = default

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            vector = self._default
            for keyword, candidate in self._vector_by_keyword.items():
                if keyword in text:
                    vector = candidate
                    break
            vectors.append(vector)
        return vectors

    def embedding_model_id(self) -> str:
        return "fake"


def test_brain_contracts_for_capabilities_returns_support_contract_and_backend_mappings(storage) -> None:
    capability = make_capability(
        "capability:confirm_agv_active_error_state",
        target_entity_ids=["entity:system:agv_fleet"],
    )
    capability = capability.model_copy(
        update={
            "support_contract": SupportContract(
                diagnostic_surface_entity_ids=["entity:system:agv_fleet"],
                preferred_surface_entity_id="entity:system:agv_fleet",
            ),
            "sql_field_notes": [
                SqlFieldNote(table_entity_id="entity:table:robot_database_model", field="State", purpose="AGV state"),
                SqlFieldNote(table_entity_id="entity:table:robot_database_model", field="ErrorCode", purpose="Active error"),
            ],
        }
    )
    storage.save_brain_records(
        [capability, make_entity("entity:system:agv_fleet")], scope="ontology_catalogs"
    )

    contracts = brain_contracts_for_capabilities(
        ["confirm_agv_active_error_state"], storage=storage
    )

    assert len(contracts) == 1
    contract = contracts[0]
    assert contract["id"] == "capability:confirm_agv_active_error_state"
    assert contract["support_contract"]["preferred_surface_entity_id"] == "entity:system:agv_fleet"
    assert contract["backend_mappings"][0]["support_read_sources"][0]["fields"] == ["State", "ErrorCode"]


def test_brain_contracts_for_capabilities_accepts_already_prefixed_ids(storage) -> None:
    capability = make_capability("capability:confirm_wcs_system_faults")
    storage.save_brain_records([capability], scope="ontology_catalogs")

    contracts = brain_contracts_for_capabilities(
        ["capability:confirm_wcs_system_faults"], storage=storage
    )

    assert len(contracts) == 1
    assert contracts[0]["id"] == "capability:confirm_wcs_system_faults"


def test_brain_contracts_for_capabilities_returns_empty_for_no_ids(storage) -> None:
    assert brain_contracts_for_capabilities(None, storage=storage) == []
    assert brain_contracts_for_capabilities([], storage=storage) == []


def test_brain_contracts_for_capabilities_returns_empty_for_unknown_id(storage) -> None:
    storage.save_brain_records([make_capability("capability:confirm_agv_active_error_state")], scope="ontology_catalogs")

    assert brain_contracts_for_capabilities(["does_not_exist"], storage=storage) == []


def test_brain_snippets_for_stage5_playbook_returns_ranked_matches(storage) -> None:
    capability = make_capability("capability:confirm_agv_active_error_state")
    storage.save_brain_records([capability], scope="ontology_catalogs")
    storage.save_embeddings(
        [{"record_id": capability.id, "record_type": "capability", "embedding_model": "m", "vector": [1.0, 0.0]}]
    )
    embeddings = FakeEmbeddingProvider({"active error": [1.0, 0.0]}, default=[0.0, 1.0])

    snippets = brain_snippets_for_stage5_playbook(
        "check for active error on the AGV", embeddings=embeddings, storage=storage
    )

    assert len(snippets) == 1
    snippet = snippets[0]
    assert snippet["id"] == "capability:confirm_agv_active_error_state"
    assert snippet["title"] == capability.name
    assert snippet["score"] > 0.9
    assert "source_refs" in snippet
    assert "text" in snippet


def test_brain_snippets_for_stage5_playbook_respects_min_score(storage) -> None:
    capability = make_capability("capability:confirm_agv_active_error_state")
    storage.save_brain_records([capability], scope="ontology_catalogs")
    storage.save_embeddings(
        [{"record_id": capability.id, "record_type": "capability", "embedding_model": "m", "vector": [1.0, 0.0]}]
    )
    # Orthogonal vector -> cosine similarity 0.0, below any reasonable floor.
    embeddings = FakeEmbeddingProvider({}, default=[0.0, 1.0])

    snippets = brain_snippets_for_stage5_playbook(
        "unrelated query text", embeddings=embeddings, storage=storage
    )

    assert snippets == []


def test_brain_snippets_for_stage5_playbook_returns_empty_for_blank_text(storage) -> None:
    embeddings = FakeEmbeddingProvider({}, default=[1.0, 0.0])

    assert brain_snippets_for_stage5_playbook("   ", embeddings=embeddings, storage=storage) == []


def test_brain_snippets_for_stage5_playbook_only_returns_known_snippet_keys(storage) -> None:
    capability = make_capability("capability:confirm_agv_active_error_state")
    storage.save_brain_records([capability], scope="ontology_catalogs")
    storage.save_embeddings(
        [{"record_id": capability.id, "record_type": "capability", "embedding_model": "m", "vector": [1.0, 0.0]}]
    )
    embeddings = FakeEmbeddingProvider({"active error": [1.0, 0.0]}, default=[0.0, 1.0])

    snippets = brain_snippets_for_stage5_playbook(
        "active error", embeddings=embeddings, storage=storage
    )

    # action_synthesis.py's _selected_ontology_entities only reads these
    # five keys -- confirms the bridge never emits an unexpected shape.
    assert set(snippets[0].keys()) == {"id", "title", "score", "source_refs", "text"}
