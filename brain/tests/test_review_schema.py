from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from brain.schemas.claim import Claim
from brain.schemas.common import ValidationStatus
from brain.schemas.entity import Entity
from brain.schemas.review import BrainReview
from brain.validators import validate_batch

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


# --- Fixture round-trip ---


def test_tote_state_conflict_review_fixture_validates() -> None:
    review = BrainReview.model_validate(load_fixture("tote_state_conflict_review.json"))
    assert review.kind.value == "conflict"
    assert review.status == "open"
    assert review.resolution is None
    assert len(review.affected_record_ids) == 2


# --- Field-level rules ---


def test_review_requires_at_least_one_affected_record_id() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["affected_record_ids"] = []
    with pytest.raises(ValidationError):
        BrainReview.model_validate(data)


def test_review_rejects_malformed_affected_record_id() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["affected_record_ids"] = ["not-a-typed-id"]
    with pytest.raises(ValidationError):
        BrainReview.model_validate(data)


def test_review_resolution_requires_resolved_status() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["resolution"] = "not_a_duplicate"
    # status is still "open" -- resolution set without resolved status is invalid
    with pytest.raises(ValidationError):
        BrainReview.model_validate(data)


def test_review_resolved_status_requires_resolution() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["status"] = "resolved"
    with pytest.raises(ValidationError):
        BrainReview.model_validate(data)


def test_review_resolved_with_resolution_is_valid() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["status"] = "resolved"
    data["resolution"] = "not_a_duplicate"
    data["resolved_by"] = "human"
    review = BrainReview.model_validate(data)
    assert review.status == "resolved"
    assert review.resolution.value == "not_a_duplicate"


def test_review_check_name_only_valid_for_audit_finding() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["check_name"] = "casing_collision"
    # kind is "conflict", not "audit_finding" -- check_name is only meaningful there
    with pytest.raises(ValidationError):
        BrainReview.model_validate(data)


def test_review_check_name_valid_for_audit_finding() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["kind"] = "audit_finding"
    data["check_name"] = "casing_collision"
    review = BrainReview.model_validate(data)
    assert review.check_name == "casing_collision"


def test_review_fields_to_rewrite_defaults_empty() -> None:
    # 2026-09-10: new field, added for RETYPE's new_entity_type carrier --
    # a fixture written before this field existed (no key present at all)
    # must still validate, confirming backward compatibility with every
    # BrainReview already persisted in Cosmos before this field existed.
    review = BrainReview.model_validate(load_fixture("tote_state_conflict_review.json"))
    assert review.fields_to_rewrite == {}


def test_review_fields_to_rewrite_round_trips() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["kind"] = "audit_finding"
    data["check_name"] = "casing_collision"
    data["status"] = "resolved"
    data["resolution"] = "retype"
    data["resolved_by"] = "agent"
    data["fields_to_rewrite"] = {"entity_type": "symptom"}

    review = BrainReview.model_validate(data)
    assert review.fields_to_rewrite == {"entity_type": "symptom"}
    round_tripped = BrainReview.model_validate(review.model_dump(mode="json"))
    assert round_tripped.fields_to_rewrite == {"entity_type": "symptom"}


# --- validate_batch: affected_record_ids must resolve ---


def _heartbeat_v1_claim() -> Claim:
    data = load_fixture("heartbeat_claim.json")
    data["id"] = "claim:tote_state:heartbeat_interval_v1"
    return Claim.model_validate(data)


def _heartbeat_v2_claim() -> Claim:
    data = load_fixture("heartbeat_claim.json")
    data["id"] = "claim:tote_state:heartbeat_interval_v2"
    return Claim.model_validate(data)


def _claim_subject_entities() -> list[Entity]:
    # The heartbeat_claim fixture's own subject_entity_id/object.entity_id
    # -- needed here so validate_claim_references (a separate check) does
    # not itself fail and mask what this test is actually checking.
    return [
        Entity.model_validate(
            {
                "id": "entity:metric:tipper_heartbeat_max",
                "type": "entity",
                "schema_version": "1.0",
                "entity_type": "metric",
                "name": "Tipper heartbeat max",
                "description": "",
                "aliases": [],
                "payload": {},
                "source_refs": ["evidence:manual_om:heartbeat_stats_section"],
                "constraints": {},
            }
        ),
        Entity.model_validate(
            {
                "id": "entity:state:tipper_wcs_synchronization_risk",
                "type": "entity",
                "schema_version": "1.0",
                "entity_type": "state",
                "name": "Tipper/WCS synchronization risk",
                "description": "",
                "aliases": [],
                "payload": {},
                "source_refs": ["evidence:manual_om:heartbeat_stats_section"],
                "constraints": {},
            }
        ),
    ]


def test_validate_batch_passes_when_review_references_resolve() -> None:
    review = BrainReview.model_validate(load_fixture("tote_state_conflict_review.json"))
    claims = [_heartbeat_v1_claim(), _heartbeat_v2_claim()]

    result = validate_batch(entities=_claim_subject_entities(), claims=claims, reviews=[review])
    assert result.valid, result.errors


def test_validate_batch_flags_review_with_unknown_affected_record_id() -> None:
    review = BrainReview.model_validate(load_fixture("tote_state_conflict_review.json"))
    # only one of the two affected claims is present in the batch
    claims = [_heartbeat_v1_claim()]

    result = validate_batch(entities=_claim_subject_entities(), claims=claims, reviews=[review])
    assert not result.valid
    assert any("heartbeat_interval_v2" in e for e in result.errors)


# --- ValidationStatus default and coverage ---


def test_brain_record_defaults_to_operational_unreviewed() -> None:
    review = BrainReview.model_validate(load_fixture("tote_state_conflict_review.json"))
    assert review.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED


def test_brain_record_accepts_explicit_validation_status() -> None:
    data = load_fixture("tote_state_conflict_review.json")
    data["validation_status"] = "catalog_authoritative"
    review = BrainReview.model_validate(data)
    assert review.validation_status == ValidationStatus.CATALOG_AUTHORITATIVE
