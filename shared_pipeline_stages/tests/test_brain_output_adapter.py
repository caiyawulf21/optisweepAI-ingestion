from __future__ import annotations

from pathlib import Path

import pytest

from brain.schemas.common import ValidationStatus
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.playbook import Playbook, PlaybookNodeType
from brain.schemas.procedure import Procedure
from brain_service.tests.conftest import make_capability, make_entity
from providers.local_storage import LocalStorageProvider
from shared_pipeline_stages.brain_output_adapter import (
    build_corpus_index,
    canonical_playbook_to_playbook,
    canonical_runbook_to_procedure,
)


@pytest.fixture()
def storage(tmp_path: Path) -> LocalStorageProvider:
    return LocalStorageProvider(root=tmp_path)


def _runbook(**overrides) -> dict:
    base = {
        "procedure_id": "proc_query_active_agv_errors_from_the_wcs_database_v1",
        "title": "Query Active AGV Errors From the WCS Database",
        "summary": "Runs the approved SELECT against SystemActiveError.",
        "procedure_type": "diagnostic",
        "role_required": "L2_support",
        "responsible_role": "L2_support",
        "supporting_roles": [],
        "audience_roles": ["L2_support"],
        "capability_tags": ["confirm_agv_active_error_state"],
        "when_to_use": "Use when active AGV errors are suspected.",
        "not_for": [],
        "steps": [
            {
                "step_number": 1,
                "title": "Run the query",
                "responsible_role": "L2_support",
                "supporting_role": "",
                "purpose": "Confirm active errors.",
                "instruction": "Open SSMS and run the approved SELECT.",
                "expected_result": "Rows returned or empty result.",
                "healthy_condition": "No active error rows.",
                "failure_condition": "One or more active error rows.",
                "actions": [
                    {
                        "action_type": "command_action",
                        "label": "Run query",
                        "exact_action": "SELECT * FROM SystemActiveError",
                        "role_required": "L2_support",
                    }
                ],
                "stop_or_escalate_if": ["Query fails to execute"],
            }
        ],
    }
    base.update(overrides)
    return base


def _seed_capability_and_role(storage) -> None:
    storage.save_brain_records(
        [
            make_capability("capability:confirm_agv_active_error_state"),
            make_entity("entity:role:l2_support", name="L2_support"),
        ],
        scope="ontology_catalogs",
    )


def test_canonical_runbook_to_procedure_builds_valid_procedure(storage) -> None:
    _seed_capability_and_role(storage)

    result = canonical_runbook_to_procedure(_runbook(), index=build_corpus_index(storage), source_id="stage7_run1")

    assert isinstance(result.evidence, EvidenceUnit)
    assert result.procedure is not None
    assert isinstance(result.procedure, Procedure)
    assert result.procedure.capability_id == "capability:confirm_agv_active_error_state"
    assert result.procedure.allowed_role_entity_ids == ["entity:role:l2_support"]
    assert result.procedure.steps[0].responsible_role_entity_id == "entity:role:l2_support"
    assert result.procedure.validation_status == ValidationStatus.OPERATIONAL_UNREVIEWED
    assert result.gaps == []
    # Full schema round-trip -- confirms nothing here bypasses Procedure's own validators.
    Procedure.model_validate(result.procedure.model_dump(mode="json"))


def test_canonical_runbook_to_procedure_reports_gap_for_unresolved_capability(storage) -> None:
    # No Capability seeded at all.
    result = canonical_runbook_to_procedure(_runbook(), index=build_corpus_index(storage), source_id="stage7_run1")

    assert result.procedure is None
    assert any("resolves to an existing Brain Capability" in gap for gap in result.gaps)
    # Evidence is still returned even when the Procedure can't be built --
    # the wrapping citation is real regardless of downstream resolution.
    assert isinstance(result.evidence, EvidenceUnit)


def test_canonical_runbook_to_procedure_reports_gap_for_unresolved_role(storage) -> None:
    storage.save_brain_records([make_capability("capability:confirm_agv_active_error_state")], scope="ontology_catalogs")

    result = canonical_runbook_to_procedure(_runbook(), index=build_corpus_index(storage), source_id="stage7_run1")

    assert result.procedure is not None
    assert result.procedure.allowed_role_entity_ids == []
    assert any("L2_support" in gap for gap in result.gaps)


def test_canonical_runbook_to_procedure_skips_when_no_steps(storage) -> None:
    _seed_capability_and_role(storage)

    result = canonical_runbook_to_procedure(_runbook(steps=[]), index=build_corpus_index(storage), source_id="stage7_run1")

    assert result.procedure is None
    assert any("no usable steps" in gap for gap in result.gaps)


def _playbook(**overrides) -> dict:
    base = {
        "playbook_id": "playbook_218550_bagout",
        "title": "Diagnose bag-out stoppage",
        "playbook_goal": "Route from a bag-out stoppage report to the right procedure.",
        "confidence": "medium",
        "nodes": [
            {
                "node_id": "node_1",
                "node_order": 1,
                "node_type": "procedure_reference",
                "title": "Query active AGV errors",
                "resolved_runbook_ids": ["proc_query_active_agv_errors_from_the_wcs_database_v1"],
                "allowed_roles": ["L2_support"],
                "branches": [
                    {
                        "branch_id": "b1",
                        "outcome": "unhealthy",
                        "condition_descriptor": "Active errors found",
                        "next_node_id": "node_2",
                    },
                    {
                        "branch_id": "b2",
                        "outcome": "healthy",
                        "condition_descriptor": "No active errors",
                        "next_node_id": None,
                    },
                ],
            },
            {
                "node_id": "node_2",
                "node_order": 2,
                "node_type": "escalation_gate",
                "title": "Escalate to L3",
                "branches": [],
            },
        ],
    }
    base.update(overrides)
    return base


def _seed_promoted_runbook(storage) -> Procedure:
    _seed_capability_and_role(storage)
    result = canonical_runbook_to_procedure(_runbook(), index=build_corpus_index(storage), source_id="stage7_run1")
    storage.save_brain_records([result.evidence, result.procedure], scope="ontology_catalogs")
    return result.procedure


def test_canonical_playbook_to_playbook_resolves_promoted_procedure_reference(storage) -> None:
    promoted = _seed_promoted_runbook(storage)

    result = canonical_playbook_to_playbook(_playbook(), index=build_corpus_index(storage), source_id="stage8_run1")

    assert result.playbook is not None
    assert isinstance(result.playbook, Playbook)
    node_1 = next(n for n in result.playbook.nodes if n.node_id == "node_1")
    assert node_1.node_type == PlaybookNodeType.PROCEDURE_REFERENCE
    assert node_1.procedure_id == promoted.id
    assert result.gaps == []
    Playbook.model_validate(result.playbook.model_dump(mode="json"))


def test_canonical_playbook_to_playbook_downgrades_node_when_procedure_not_promoted(storage) -> None:
    # No Procedure promoted yet -- resolved_runbook_ids won't match anything.
    result = canonical_playbook_to_playbook(_playbook(), index=build_corpus_index(storage), source_id="stage8_run1")

    assert result.playbook is not None
    node_1 = next(n for n in result.playbook.nodes if n.node_id == "node_1")
    assert node_1.node_type == PlaybookNodeType.DIAGNOSTIC_DECISION
    assert node_1.procedure_id is None
    assert any("have not been promoted" in gap for gap in result.gaps)


def test_canonical_playbook_to_playbook_clears_dangling_branch_target(storage) -> None:
    _seed_promoted_runbook(storage)
    playbook = _playbook(
        nodes=[
            {
                "node_id": "node_1",
                "node_order": 1,
                "node_type": "diagnostic_decision",
                "title": "Check something",
                "branches": [
                    {
                        "branch_id": "b1",
                        "outcome": "unhealthy",
                        "condition_descriptor": "bad",
                        "next_node_id": "node_does_not_exist",
                    }
                ],
            }
        ]
    )

    result = canonical_playbook_to_playbook(playbook, index=build_corpus_index(storage), source_id="stage8_run1")

    assert result.playbook is not None
    assert result.playbook.nodes[0].branches[0].next_node_id is None
    assert any("not a node in this playbook" in gap for gap in result.gaps)


def test_canonical_playbook_to_playbook_skips_when_no_nodes(storage) -> None:
    result = canonical_playbook_to_playbook(_playbook(nodes=[]), index=build_corpus_index(storage), source_id="stage8_run1")

    assert result.playbook is None
    assert any("no usable nodes" in gap for gap in result.gaps)


def test_canonical_playbook_to_playbook_maps_branching_condition_node_type(storage) -> None:
    playbook = _playbook(
        nodes=[
            {
                "node_id": "node_1",
                "node_order": 1,
                "node_type": "branching_condition",
                "title": "Branch here",
                "branches": [],
            }
        ]
    )

    result = canonical_playbook_to_playbook(playbook, index=build_corpus_index(storage), source_id="stage8_run1")

    assert result.playbook is not None
    assert result.playbook.nodes[0].node_type == PlaybookNodeType.DIAGNOSTIC_DECISION
