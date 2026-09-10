from __future__ import annotations

from brain.schemas.entity import EntityType
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import ReviewResolution
from brain_service.audit import AuditResolutionResponse, find_audit_candidates, resolve_audit_candidate
from brain_service.tests.conftest import ScriptedLLM, make_entity


def test_finds_normalized_name_collision(storage) -> None:
    storage.save_brain_records(
        [
            make_entity("entity:system:geekagv", name="GeekAgv"),
            make_entity("entity:system:geek_agv", name="geek_agv"),
        ],
        scope="operational_sources/test",
    )

    findings = find_audit_candidates(storage)

    assert any(f.check_name == "normalized_name_collision" for f in findings)


def test_no_false_positive_for_distinct_names(storage) -> None:
    storage.save_brain_records(
        [make_entity("entity:system:a", name="Alpha"), make_entity("entity:system:b", name="Beta")],
        scope="operational_sources/test",
    )

    findings = find_audit_candidates(storage)

    assert findings == []


def test_finds_cross_type_same_name(storage) -> None:
    same_name_component = make_entity("entity:component:widget", name="Widget")
    same_name_system = make_entity("entity:system:widget", name="Widget")
    storage.save_brain_records([same_name_component, same_name_system], scope="operational_sources/test")

    findings = find_audit_candidates(storage)

    cross_type = [f for f in findings if f.check_name == "cross_type_same_name"]
    assert len(cross_type) == 1
    assert set(cross_type[0].affected_record_ids) == {"entity:component:widget", "entity:system:widget"}


def test_finds_applies_to_self_echo(storage) -> None:
    parent = make_entity("entity:system:parent")
    child = make_entity("entity:component:child")
    storage.save_brain_records([parent, child], scope="operational_sources/test")
    rel = Relationship(
        id="relationship:child:applies_to:parent",
        from_id="entity:component:child",
        relationship_type=RelationshipType.APPLIES_TO,
        to_id="entity:system:parent",
        source_refs=["evidence:test:seed"],
    )
    storage.save_brain_records([rel], scope="operational_sources/test")

    findings = find_audit_candidates(storage)

    assert any(f.check_name == "applies_to_self_echo" for f in findings)


def test_claim_shaped_check_only_looks_at_name_not_description(storage) -> None:
    """This check must never flag a well-formed entity whose DESCRIPTION
    happens to be a full sentence -- that is normal, correct prose, not a
    category error. Regression test for the bug found during this tool's
    own build: calling is_claim_shaped() on `description` instead of `name`
    produced 715/775 false positives against the real corpus."""
    entity = make_entity(
        "entity:system:wcs_api",
        name="wcs_api",
        description="Logical catalog of OptiSweep System/AGV/Tote APIs, executed via Apidog.",
    )
    storage.save_brain_records([entity], scope="operational_sources/test")

    findings = find_audit_candidates(storage)

    assert not any(f.check_name == "claim_shaped_entity" for f in findings)


def test_claim_shaped_check_flags_a_verb_first_name(storage) -> None:
    entity = make_entity(
        "entity:symptom:confirm_the_agv_active_error",
        name="Confirm the AGV active error",
        description="fine",
    )
    storage.save_brain_records([entity], scope="operational_sources/test")

    findings = find_audit_candidates(storage)

    claim_shaped = [f for f in findings if f.check_name == "claim_shaped_entity"]
    assert len(claim_shaped) == 1
    assert claim_shaped[0].affected_record_ids == [entity.id]


def test_record_ids_filter_narrows_returned_findings_not_the_scan(storage) -> None:
    storage.save_brain_records(
        [
            # First collision pair.
            make_entity("entity:system:geekagv", name="GeekAgv"),
            make_entity("entity:system:geek_agv", name="geek_agv"),
            # Second, unrelated collision pair -- must also be found (the
            # scan itself is never scoped down), but excluded once filtered
            # to only the first pair's id.
            make_entity("entity:system:sorterside", name="SorterSide"),
            make_entity("entity:system:sorter_side", name="sorter_side"),
        ],
        scope="operational_sources/test",
    )

    all_findings = find_audit_candidates(storage)
    filtered = find_audit_candidates(storage, record_ids=["entity:system:geekagv"])

    assert len(all_findings) == 2
    assert len(filtered) == 1
    assert all("entity:system:geekagv" in f.affected_record_ids for f in filtered)


def test_resolve_audit_candidate_proposes_without_writing(storage, monkeypatch) -> None:
    storage.save_brain_records(
        [
            make_entity("entity:system:geekagv", name="GeekAgv"),
            make_entity("entity:system:geek_agv", name="geek_agv"),
        ],
        scope="operational_sources/test",
    )
    findings = find_audit_candidates(storage)
    finding = findings[0]

    llm = ScriptedLLM(
        {
            AuditResolutionResponse: [
                AuditResolutionResponse(resolution=ReviewResolution.MERGE, rationale="same real thing")
            ]
        }
    )

    resolved = resolve_audit_candidate(llm, storage, finding)

    assert resolved.resolution == ReviewResolution.MERGE
    assert resolved.resolved_by == "agent"
    assert resolved.status == "resolved"
    # Proposing must not itself apply the merge -- both original entities
    # still exist in storage untouched.
    still_present = storage.load_brain_records(scope="operational_sources/test")
    assert {r.id for r in still_present} == {"entity:system:geekagv", "entity:system:geek_agv"}
