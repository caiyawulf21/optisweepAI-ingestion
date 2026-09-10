"""Call each MCP tool function directly (bypassing the MCP transport) with
fake providers -- confirms the wrapper's plumbing (validate input, call
exactly one brain_service.* function, shape the return) without needing a
real MCP client harness or real Azure credentials.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from brain.id_generation import make_id
from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.entity import Entity, EntityType
from brain.schemas.procedure import Procedure, ProcedureStep
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import ReviewKind, ReviewResolution
from brain_service.tests.conftest import ScriptedLLM
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    DraftedPlaybook,
    DraftedPlaybookNode,
    DraftedProcedure,
    DraftedProcedureStep,
    EvidenceCandidate,
    ExtractEvidenceResult,
    ReconciliationDecision,
    ReconciliationOutcome,
)
from mcp_server import tools
from providers.local_storage import LocalStorageProvider


@pytest.fixture()
def storage(tmp_path: Path) -> LocalStorageProvider:
    provider = LocalStorageProvider(root=tmp_path)
    provider.save_brain_records(
        [
            Entity(
                id="entity:system:seed",
                entity_type=EntityType.SYSTEM,
                name="Seed System",
                description="test",
                source_refs=["evidence:test:seed"],
            )
        ],
        scope="operational_sources/seed",
    )
    return provider


@pytest.fixture(autouse=True)
def _patch_storage_provider(monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider) -> None:
    monkeypatch.setattr("mcp_server.tools.get_storage_provider", lambda: storage)


def test_extract_evidence_calls_extraction_module(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = ExtractEvidenceResult(
        candidates=[
            EvidenceCandidate(
                evidence_kind="sme_note", content_text="x", is_verbatim=False, raw_claim_candidates=["x"]
            )
        ]
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({ExtractEvidenceResult: [expected]}))

    result = tools.tool_extract_evidence({"text": "some packet"})

    assert result["candidates"][0]["content_text"] == "x"


def test_classify_candidate_calls_classification_module(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM,
        proposed_fields={},
        confidence="high",
        rationale="test",
        source_evidence_ids=["evidence:test:seed"],
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({ClassifiedCandidate: [expected]}))

    result = tools.tool_classify_candidate("some claim", "evidence:test:1")

    assert result["record_kind"] == "claim"
    assert result["confidence"] == "high"


def test_reconcile_candidate_calls_reconciliation_module(monkeypatch: pytest.MonkeyPatch) -> None:
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM, proposed_fields={}, confidence="medium", rationale="x"
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.REINFORCE,
        classified=classified,
        affected_record_ids=["entity:system:seed"],
        rationale="already known",
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({ReconciliationDecision: [decision]}))

    result = tools.tool_reconcile_candidate(classified.model_dump(mode="json"))

    assert result["outcome"] == "reinforce"


def test_validate_and_prepare_for_review_returns_open_brain_review(storage: LocalStorageProvider) -> None:
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM,
        proposed_fields={},
        confidence="medium",
        rationale="x",
        source_evidence_ids=["evidence:test:seed"],
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.PATCH,
        classified=classified,
        affected_record_ids=["entity:system:seed"],
        patch_fields={"aliases": ["Alt name"]},
        rationale="adds an alias",
    )

    result = tools.tool_validate_and_prepare_for_review(decision.model_dump(mode="json"))

    assert result["status"] == "open"
    assert "VALIDATION FAILED" not in result["proposed_change"]


def test_find_audit_candidates_returns_findings_list(storage: LocalStorageProvider) -> None:
    storage.save_brain_records(
        [
            Entity(
                id="entity:system:dup_a",
                entity_type=EntityType.SYSTEM,
                name="DupName",
                description="x",
                source_refs=["evidence:test:seed"],
            ),
            Entity(
                id="entity:system:dup_b",
                entity_type=EntityType.SYSTEM,
                name="dup_name",
                description="x",
                source_refs=["evidence:test:seed"],
            ),
        ],
        scope="operational_sources/seed",
    )

    result = tools.tool_find_audit_candidates()

    assert any(f["check_name"] == "normalized_name_collision" for f in result["findings"])


def test_resolve_audit_candidate_proposes_resolution(monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider) -> None:
    storage.save_brain_records(
        [
            Entity(id="entity:system:a", entity_type=EntityType.SYSTEM, name="Xx", description="a", source_refs=["evidence:test:seed"]),
            Entity(id="entity:system:b", entity_type=EntityType.SYSTEM, name="xx", description="b", source_refs=["evidence:test:seed"]),
        ],
        scope="operational_sources/seed",
    )
    findings = tools.tool_find_audit_candidates()["findings"]
    assert findings

    from brain_service.audit import AuditResolutionResponse

    resolution = AuditResolutionResponse(resolution=ReviewResolution.NOT_A_DUPLICATE, rationale="different things")
    monkeypatch.setattr(
        "mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({AuditResolutionResponse: [resolution]})
    )

    result = tools.tool_resolve_audit_candidate(findings[0])

    assert result["resolution"] == "not_a_duplicate"
    assert result["status"] == "resolved"


def test_run_migration_batch_returns_report(monkeypatch: pytest.MonkeyPatch) -> None:
    extraction = ExtractEvidenceResult(candidates=[])
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({ExtractEvidenceResult: [extraction]}))

    result = tools.tool_run_migration_batch(["item_1"], {"item_1": {"text": "x"}})

    assert result["outcomes"][0]["item"] == "item_1"
    assert result["outcomes"][0]["status"] == "succeeded"


def test_draft_procedure_returns_procedure_without_writing_by_default(
    monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider
) -> None:
    storage.save_brain_records(
        [
            Capability(
                id="capability:confirm_seed_health",
                name="confirm_seed_health",
                capability_kind=CapabilityKind.DIAGNOSTIC,
                source_refs=["evidence:test:seed"],
            )
        ],
        scope="ontology_catalogs",
    )
    drafted = DraftedProcedure(
        title="Confirm seed health",
        steps=[
            DraftedProcedureStep(
                step_number=1,
                title="Check seed status",
                instruction="Open the status screen.",
                source_refs=["evidence:test:seed"],
            )
        ],
        rationale="test",
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({DraftedProcedure: [drafted]}))

    result = tools.tool_draft_procedure("capability:confirm_seed_health", "case_test", "incidents/case_test")

    assert result["written"] is False
    assert result["procedure"]["capability_id"] == "capability:confirm_seed_health"
    assert storage.load_brain_records(scope="incidents/case_test") == []


def test_draft_procedure_writes_when_requested(
    monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider
) -> None:
    storage.save_brain_records(
        [
            Capability(
                id="capability:confirm_seed_health",
                name="confirm_seed_health",
                capability_kind=CapabilityKind.DIAGNOSTIC,
                source_refs=["evidence:test:seed"],
            )
        ],
        scope="ontology_catalogs",
    )
    drafted = DraftedProcedure(
        title="Confirm seed health",
        steps=[
            DraftedProcedureStep(
                step_number=1,
                title="Check seed status",
                instruction="Open the status screen.",
                source_refs=["evidence:test:seed"],
            )
        ],
        rationale="test",
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({DraftedProcedure: [drafted]}))

    result = tools.tool_draft_procedure(
        "capability:confirm_seed_health", "case_test", "incidents/case_test", write=True
    )

    assert result["written"] is True
    loaded_ids = {r.id for r in storage.load_brain_records(scope="incidents/case_test")}
    assert result["procedure"]["id"] in loaded_ids


def test_draft_playbook_returns_playbook_without_writing_by_default(
    monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider
) -> None:
    storage.save_brain_records(
        [
            Entity(
                id="entity:symptom:seed_fault",
                entity_type=EntityType.SYMPTOM,
                name="Seed fault",
                description="test",
                source_refs=["evidence:test:seed"],
            ),
            Capability(
                id="capability:confirm_seed_health",
                name="confirm_seed_health",
                capability_kind=CapabilityKind.DIAGNOSTIC,
                source_refs=["evidence:test:seed"],
            ),
            Relationship(
                id=make_id("relationship", "entity:symptom:seed_fault", "may_indicate", "capability:confirm_seed_health"),
                from_id="entity:symptom:seed_fault",
                relationship_type=RelationshipType.MAY_INDICATE,
                to_id="capability:confirm_seed_health",
                source_refs=["evidence:test:seed"],
            ),
            Procedure(
                id="procedure:confirm_seed_health:seed_1",
                capability_id="capability:confirm_seed_health",
                procedure_type=CapabilityKind.DIAGNOSTIC,
                title="Confirm seed health",
                steps=[
                    ProcedureStep(
                        step_number=1, title="Check", instruction="Check it.", source_refs=["evidence:test:seed"]
                    )
                ],
                source_refs=["evidence:test:seed"],
            ),
        ],
        scope="operational_sources/seed",
    )
    drafted = DraftedPlaybook(
        title="Diagnose seed fault",
        entry_symptom_entity_ids=["entity:symptom:seed_fault"],
        nodes=[
            DraftedPlaybookNode(
                node_id="run_procedure",
                node_order=1,
                node_type="procedure_reference",
                title="Run confirm seed health",
                procedure_id="procedure:confirm_seed_health:seed_1",
                source_refs=["evidence:test:seed"],
            )
        ],
        entry_node_id="run_procedure",
        rationale="test",
    )
    monkeypatch.setattr("mcp_server.tools.get_llm_provider", lambda: ScriptedLLM({DraftedPlaybook: [drafted]}))

    result = tools.tool_draft_playbook(
        ["entity:symptom:seed_fault"], "case_test", "incidents/case_test"
    )

    assert result["written"] is False
    assert result["playbook"]["entry_symptom_entity_ids"] == ["entity:symptom:seed_fault"]
    assert storage.load_brain_records(scope="incidents/case_test") == []


def test_get_brain_context_returns_context_packet(storage: LocalStorageProvider) -> None:
    result = tools.tool_get_brain_context(task={"kind": "test"}, entity_ids=["entity:system:seed"])

    assert result["entities"] == ["entity:system:seed"]


def test_get_brain_context_with_query_text_uses_embedding_provider(
    monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider
) -> None:
    storage.save_embeddings(
        [{"record_id": "entity:system:seed", "record_type": "entity", "embedding_model": "m", "vector": [1.0, 0.0]}]
    )

    class FakeEmbeddingProvider:
        def embed_texts(self, texts):
            return [[1.0, 0.0] for _ in texts]

        def embedding_model_id(self):
            return "fake"

    monkeypatch.setattr("mcp_server.providers_config.get_embedding_provider", lambda: FakeEmbeddingProvider())

    result = tools.tool_get_brain_context(task={"kind": "test"}, query_text="something about seed")

    assert result["entities"] == ["entity:system:seed"]


def test_get_brain_context_without_query_text_never_calls_embedding_provider(
    monkeypatch: pytest.MonkeyPatch, storage: LocalStorageProvider
) -> None:
    def fail_if_called():
        raise AssertionError("get_embedding_provider should not be called when query_text is None")

    monkeypatch.setattr("mcp_server.providers_config.get_embedding_provider", fail_if_called)

    result = tools.tool_get_brain_context(task={"kind": "test"}, entity_ids=["entity:system:seed"])

    assert result["entities"] == ["entity:system:seed"]


def test_validate_brain_records_reports_valid_batch(storage: LocalStorageProvider) -> None:
    entity_dict = Entity(
        id="entity:system:new_one",
        entity_type=EntityType.SYSTEM,
        name="New One",
        description="x",
        source_refs=["evidence:test:seed"],
    ).model_dump(mode="json")

    result = tools.tool_validate_brain_records({"entities": [entity_dict]})

    assert result["valid"] is True
    assert result["errors"] == []


def test_prepare_sme_review_persists_and_returns_review(storage: LocalStorageProvider) -> None:
    result = tools.tool_prepare_sme_review(
        candidate_record_ids=["entity:system:seed"], kind="gap", proposed_change="needs review"
    )

    assert result["kind"] == "gap"
    assert result["status"] == "open"
    loaded = storage.load_brain_records(scope="reviews/prepared")
    assert any(r.id == result["id"] for r in loaded)


def test_get_ingestion_run_returns_none_when_missing(storage: LocalStorageProvider) -> None:
    assert tools.tool_get_ingestion_run("does_not_exist") is None


def test_get_ingestion_run_returns_saved_run(storage: LocalStorageProvider) -> None:
    storage.save_ingestion_run({"run_id": "run_42", "status": "ok"})
    assert tools.tool_get_ingestion_run("run_42") == {"run_id": "run_42", "status": "ok"}
