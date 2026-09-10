"""Call each route handler function directly (bypassing FastAPI/HTTP
transport) with fake/local providers -- mirrors
mcp_server/tests/test_tools.py's own pattern."""

from __future__ import annotations

from pathlib import Path

import pytest

from brain.schemas.common import ValidationStatus
from brain.schemas.entity import Entity, EntityType
from brain.schemas.review import BrainReview, ReviewKind, ReviewResolution
from brain_service.tests.conftest import ScriptedLLM, make_entity
from brain_service.types import (
    ClassifiedCandidate,
    ClassifiedRecordKind,
    EvidenceCandidate,
    ExtractEvidenceResult,
    ReconciliationDecision,
    ReconciliationOutcome,
)
from providers.local_storage import LocalStorageProvider

from http_server import routes
from http_server.models import (
    ContextRetrieveRequest,
    FeedbackEvent,
    ReviewResolveRequest,
    TroubleshootRequest,
)


@pytest.fixture()
def storage(tmp_path: Path) -> LocalStorageProvider:
    provider = LocalStorageProvider(root=tmp_path)
    provider.save_brain_records(
        [make_entity("entity:system:seed", entity_type=EntityType.SYSTEM)],
        scope="operational_sources/seed",
    )
    return provider


class _NullEmbeddingProvider:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]

    def embedding_model_id(self) -> str:
        return "fake"


def test_context_retrieve_returns_hydrated_excerpts_not_bare_ids(storage) -> None:
    entity = make_entity("entity:system:approved").model_copy(
        update={"validation_status": ValidationStatus.SME_APPROVED}
    )
    storage.save_brain_records([entity], scope="ontology_catalogs")

    request = ContextRetrieveRequest(query_text="test query", entity_ids=[entity.id])
    result = routes.handle_context_retrieve(request, storage=storage, embeddings=_NullEmbeddingProvider())

    assert result.excerpt_count >= 1
    assert any(e.id == entity.id and e.label == "approved" for e in result.excerpts)
    # Critical response rule: never ID-only -- every excerpt carries real text.
    assert all(e.text for e in result.excerpts)


def test_troubleshoot_seeds_query_from_session_signals(storage) -> None:
    entity = make_entity("entity:system:seed")
    storage.save_brain_records([entity], scope="operational_sources/seed")

    request = TroubleshootRequest(
        session_id="session-1",
        current_node_id="node_3",
        observed_signals=["AGV active error confirmed"],
        entity_ids=[entity.id],
    )
    result = routes.handle_troubleshoot(request, storage=storage, embeddings=_NullEmbeddingProvider())

    assert result.task["session_id"] == "session-1"
    assert result.task["current_node_id"] == "node_3"


def test_feedback_runs_create_chain_and_returns_review_ids(storage) -> None:
    extraction = ExtractEvidenceResult(
        candidates=[
            EvidenceCandidate(
                evidence_kind="sme_note", content_text="feedback text", is_verbatim=False,
                raw_claim_candidates=["feedback text"],
            )
        ]
    )
    classified = ClassifiedCandidate(
        record_kind=ClassifiedRecordKind.CLAIM, proposed_fields={}, confidence="low", rationale="x",
        source_evidence_ids=["evidence:test:app_feedback_seed"],
    )
    decision = ReconciliationDecision(
        outcome=ReconciliationOutcome.GAP, classified=classified, rationale="nothing to attach to",
    )
    llm = ScriptedLLM(
        {
            ExtractEvidenceResult: [extraction],
            ClassifiedCandidate: [classified],
            ReconciliationDecision: [decision],
        }
    )

    event = FeedbackEvent(
        session_id="session-1", interaction_id="interaction-1", text="feedback text", targets=["node_3"],
    )
    result = routes.handle_feedback(event, llm=llm, storage=storage)

    assert result.status in {"succeeded", "needs_human_review"}
    assert len(result.review_ids) == 1


def test_list_reviews_filters_by_status_and_reports_open_count(storage) -> None:
    open_review = BrainReview(
        id="review:gap:open1", kind=ReviewKind.GAP, affected_record_ids=["entity:system:seed"],
        proposed_change="x", status="open",
    )
    resolved_review = BrainReview(
        id="review:gap:resolved1", kind=ReviewKind.GAP, affected_record_ids=["entity:system:seed"],
        proposed_change="y", status="resolved", resolution=ReviewResolution.APPROVED, resolved_by="human",
    )
    storage.save_brain_records([open_review, resolved_review], scope="reviews/test")

    open_only = routes.handle_list_reviews(storage=storage, status="open")
    assert len(open_only.reviews) == 1
    assert open_only.reviews[0].id == open_review.id
    assert open_only.open_count == 1

    resolved_only = routes.handle_list_reviews(storage=storage, status="resolved")
    assert len(resolved_only.reviews) == 1
    # open_count reflects the TOTAL open count regardless of the status filter applied.
    assert resolved_only.open_count == 1


def test_resolve_review_executes_merge_and_returns_mutated_ids(storage) -> None:
    winner = make_entity("entity:system:winner", description="Winner's own description.")
    loser = make_entity("entity:system:loser", description="").model_copy(
        update={"aliases": ["Loser Alias"]}
    )
    review = BrainReview(
        id="review:audit_finding:dup", kind=ReviewKind.AUDIT_FINDING, check_name="normalized_name_collision",
        affected_record_ids=[winner.id, loser.id], proposed_change="possible duplicate", status="open",
    )
    storage.save_brain_records([winner, loser, review], scope="reviews/test")

    request = ReviewResolveRequest(resolution="merge", winner_record_id=winner.id)
    result = routes.handle_resolve_review(review.id, request, llm=ScriptedLLM({}), storage=storage)

    assert result.applied is True
    assert result.resolution == "merge"
    # winner actually changes (gains loser's alias), so it's reported mutated too --
    # not just the deprecated loser.
    assert winner.id in result.mutated_record_ids
    assert loser.id in result.mutated_record_ids


def test_resolve_review_records_but_does_not_apply_reclassify(storage) -> None:
    entity = make_entity("entity:system:seed")
    review = BrainReview(
        id="review:audit_finding:reclassify", kind=ReviewKind.AUDIT_FINDING, check_name="claim_shaped_entity",
        affected_record_ids=[entity.id], proposed_change="looks miscategorized", status="open",
    )
    storage.save_brain_records([entity, review], scope="reviews/test")

    request = ReviewResolveRequest(resolution="reclassify")
    result = routes.handle_resolve_review(review.id, request, llm=ScriptedLLM({}), storage=storage)

    assert result.applied is False
    assert result.mutated_record_ids == []


def test_resolve_review_executes_retype_with_new_entity_type(storage) -> None:
    entity = Entity(
        id="entity:state:seed", entity_type=EntityType.STATE, name="seed", description="test",
        source_refs=["evidence:test:seed"],
    )
    review = BrainReview(
        id="review:audit_finding:retype", kind=ReviewKind.AUDIT_FINDING, check_name="claim_shaped_entity",
        affected_record_ids=[entity.id], proposed_change="looks miscategorized", status="open",
    )
    storage.save_brain_records([entity, review], scope="reviews/test")

    request = ReviewResolveRequest(resolution="retype", new_entity_type="symptom")
    result = routes.handle_resolve_review(review.id, request, llm=ScriptedLLM({}), storage=storage)

    assert result.applied is True
    assert "entity:symptom:seed" in result.mutated_record_ids


def test_resolve_review_retype_raises_without_new_entity_type(storage) -> None:
    entity = Entity(
        id="entity:state:seed", entity_type=EntityType.STATE, name="seed", description="test",
        source_refs=["evidence:test:seed"],
    )
    review = BrainReview(
        id="review:audit_finding:retype", kind=ReviewKind.AUDIT_FINDING, check_name="claim_shaped_entity",
        affected_record_ids=[entity.id], proposed_change="looks miscategorized", status="open",
    )
    storage.save_brain_records([entity, review], scope="reviews/test")

    request = ReviewResolveRequest(resolution="retype")
    with pytest.raises(ValueError, match="new_entity_type"):
        routes.handle_resolve_review(review.id, request, llm=ScriptedLLM({}), storage=storage)


def test_resolve_review_raises_not_found_for_unknown_id(storage) -> None:
    with pytest.raises(routes.ReviewNotFoundError):
        routes.handle_resolve_review(
            "review:does:not_exist", ReviewResolveRequest(), llm=ScriptedLLM({}), storage=storage
        )
