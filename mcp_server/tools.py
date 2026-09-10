"""The MCP tool functions. Thin wrappers only -- each validates input, calls
exactly one brain_service.* function (or, for the two ingest_* orchestration
tools, the existing pipeline CLI script as a subprocess), and shapes the
return as plain-JSON-serializable dicts. No business logic here (API-neutral
doc Step 5: "The MCP server should call the Brain service and existing
pipelines. It should not contain separate business logic.")
"""

from __future__ import annotations

import os
import subprocess
import sys
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any

from brain.schemas.relationship import RelationshipType
from brain_service.audit import find_audit_candidates, resolve_audit_candidate
from brain_service.classification import classify_candidate
from brain_service.context import get_brain_context
from brain_service.extraction import extract_evidence
from brain_service.migration import run_migration_batch
from brain_service.playbook_drafting import build_playbook_record, draft_playbook, write_drafted_playbook
from brain_service.procedure_drafting import build_procedure_record, draft_procedure, write_drafted_procedure
from brain_service.reconciliation import reconcile_candidate
from brain_service.review import build_review
from brain_service.validation import validate_and_prepare_for_review, validate_records
from brain.schemas.review import ReviewKind
from mcp_server.providers_config import get_llm_provider, get_storage_provider

REPO_ROOT = Path(__file__).resolve().parents[1]


# --- The seven ingestion/Brain tools ---------------------------------------


def tool_extract_evidence(source_packet: dict[str, Any]) -> dict[str, Any]:
    result = extract_evidence(get_llm_provider(), source_packet)
    return result.model_dump(mode="json")


def tool_classify_candidate(
    candidate_text: str,
    evidence_id: str,
    likely_entity_ids: list[str] | None = None,
) -> dict[str, Any]:
    result = classify_candidate(
        get_llm_provider(),
        get_storage_provider(),
        candidate_text=candidate_text,
        evidence_id=evidence_id,
        likely_entity_ids=likely_entity_ids,
    )
    return result.model_dump(mode="json")


def tool_reconcile_candidate(classified: dict[str, Any]) -> dict[str, Any]:
    from brain_service.types import ClassifiedCandidate

    result = reconcile_candidate(get_llm_provider(), get_storage_provider(), ClassifiedCandidate.model_validate(classified))
    return result.model_dump(mode="json")


def tool_validate_and_prepare_for_review(reconciled: dict[str, Any]) -> dict[str, Any]:
    from brain_service.types import ReconciliationDecision

    review = validate_and_prepare_for_review(get_storage_provider(), ReconciliationDecision.model_validate(reconciled))
    return review.model_dump(mode="json")


def tool_find_audit_candidates(record_ids: list[str] | None = None) -> dict[str, Any]:
    findings = find_audit_candidates(get_storage_provider(), record_ids=record_ids)
    return {"findings": [f.model_dump(mode="json") for f in findings]}


def tool_resolve_audit_candidate(review: dict[str, Any]) -> dict[str, Any]:
    from brain.schemas.review import BrainReview

    resolved = resolve_audit_candidate(get_llm_provider(), get_storage_provider(), BrainReview.model_validate(review))
    return resolved.model_dump(mode="json")


def tool_run_migration_batch(items: list[str], source_packets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """`source_packets` maps each item id to its already-loaded source
    packet -- the MCP boundary can't accept a Python callable the way
    run_migration_batch's own `load_source_packet` parameter does, so the
    caller supplies packets up front instead."""
    report = run_migration_batch(
        get_llm_provider(),
        get_storage_provider(),
        items,
        load_source_packet=lambda item: source_packets[item],
    )
    return asdict(report)


# --- Tool 8: draft_procedure (drafts FROM Brain, not the static ontology --
# catalog -- AGENT_DESIGN_NOTES.md §5/§5.1) -----------------------------


def tool_draft_procedure(
    capability_id: str,
    distinguishing_token: str,
    scope: str,
    extra_source_evidence_ids: list[str] | None = None,
    write: bool = False,
) -> dict[str, Any]:
    """Drafts a Procedure for `capability_id`, grounded in that Capability's
    own fields plus retrieved Brain context. `write=False` (default)
    returns the drafted+constructed Procedure for inspection without
    persisting -- set `write=True` once satisfied with `gaps`/steps to
    also write the record and its NEW_CANDIDATE review into `scope`."""
    storage = get_storage_provider()
    drafted = draft_procedure(
        get_llm_provider(),
        storage,
        capability_id=capability_id,
        distinguishing_token=distinguishing_token,
        extra_source_evidence_ids=extra_source_evidence_ids,
    )
    source_evidence_ids = extra_source_evidence_ids or [
        ref for step in drafted.steps for ref in step.source_refs
    ]
    record = build_procedure_record(
        drafted,
        storage,
        capability_id=capability_id,
        distinguishing_token=distinguishing_token,
        source_evidence_ids=source_evidence_ids,
    )
    if write:
        write_drafted_procedure(storage, record, scope=scope)
    return {
        "procedure": record.model_dump(mode="json"),
        "rationale": drafted.rationale,
        "gaps": drafted.gaps,
        "written": write,
    }


# --- Tool 9: draft_playbook (drafts symptom-driven branching FROM Brain's --
# own graph + already-drafted Procedures -- AGENT_DESIGN_NOTES.md §5.2) ---


def tool_draft_playbook(
    entry_symptom_entity_ids: list[str],
    distinguishing_token: str,
    scope: str,
    write: bool = False,
) -> dict[str, Any]:
    """Drafts a Playbook routing from `entry_symptom_entity_ids` to
    already-existing Procedures, grounded in the symptom graph
    (MAY_INDICATE/VERIFIES/CAUSES/CONTRIBUTES_TO relationships) plus each
    reachable Capability's own already-drafted Procedures. `write=False`
    (default) returns the drafted+constructed Playbook for inspection
    without persisting -- set `write=True` once satisfied with `gaps`/
    nodes to also write the record and its NEW_CANDIDATE review into
    `scope`."""
    storage = get_storage_provider()
    drafted = draft_playbook(
        get_llm_provider(),
        storage,
        entry_symptom_entity_ids=entry_symptom_entity_ids,
        distinguishing_token=distinguishing_token,
    )
    source_evidence_ids = [ref for node in drafted.nodes for ref in node.source_refs]
    record = build_playbook_record(
        drafted,
        storage,
        distinguishing_token=distinguishing_token,
        source_evidence_ids=source_evidence_ids,
    )
    if write:
        write_drafted_playbook(storage, record, scope=scope)
    return {
        "playbook": record.model_dump(mode="json"),
        "rationale": drafted.rationale,
        "gaps": drafted.gaps,
        "written": write,
    }


# --- get_brain_context, validate_brain_records, prepare_sme_review --------


def tool_get_brain_context(
    task: dict[str, Any],
    entity_ids: list[str] | None = None,
    relationship_types: list[str] | None = None,
    hops: int = 1,
    query_text: str | None = None,
) -> dict[str, Any]:
    from mcp_server.providers_config import get_embedding_provider

    parsed_types = [RelationshipType(t) for t in relationship_types] if relationship_types else None
    packet = get_brain_context(
        get_storage_provider(),
        task=task,
        entity_ids=entity_ids,
        relationship_types=parsed_types,
        hops=hops,
        query_text=query_text,
        embeddings=get_embedding_provider() if query_text else None,
    )
    return packet.model_dump(mode="json")


def tool_validate_brain_records(records_by_type: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    from brain.validators import BrainRecordUnion
    from brain.schemas.capability import Capability
    from brain.schemas.claim import Claim
    from brain.schemas.entity import Entity
    from brain.schemas.evidence_unit import EvidenceUnit
    from brain.schemas.playbook import Playbook
    from brain.schemas.procedure import Procedure
    from brain.schemas.relationship import Relationship
    from brain.schemas.review import BrainReview

    model_by_key = {
        "evidence_units": EvidenceUnit,
        "entities": Entity,
        "claims": Claim,
        "relationships": Relationship,
        "capabilities": Capability,
        "procedures": Procedure,
        "playbooks": Playbook,
        "reviews": BrainReview,
    }
    parsed = {
        key: [model_by_key[key].model_validate(row) for row in rows]
        for key, rows in records_by_type.items()
        if key in model_by_key
    }
    result = validate_records(parsed)
    return {"valid": result.valid, "errors": result.errors}


def tool_prepare_sme_review(
    candidate_record_ids: list[str],
    kind: str,
    proposed_change: str,
) -> dict[str, Any]:
    review = build_review(
        kind=ReviewKind(kind),
        affected_record_ids=candidate_record_ids,
        proposed_change=proposed_change,
    )
    get_storage_provider().save_brain_records([review], scope="reviews/prepared")
    return review.model_dump(mode="json")


# --- Ingestion run bookkeeping ----------------------------------------------


def tool_get_ingestion_run(run_id: str) -> dict[str, Any] | None:
    return get_storage_provider().load_ingestion_run(run_id)


# --- Pipeline orchestration: wraps the EXISTING CLI scripts, per plan §1 --
# ("no new hand-written, source-shape-specific migration script") -- these
# do not reimplement per-stage argument wiring, they turn BRAIN_INGESTION_ENABLED
# on and invoke the same CLI entrypoint a human would run.


def tool_ingest_incident_pdf(
    source_pdf_path: str,
    case_id: str,
    site_code: str = "ups_haslet_tx",
    output_dir: str | None = None,
    stages: str = "1,2,2.5,3,4,5,6,8",
    run_shared_publish: bool = False,
    publish_to_cosmos: bool = False,
    publish_scope: str = "all",
) -> dict[str, Any]:
    """One straight call covering the full incidence pipeline: per-source
    Stages 1-8 (Azure Computer Vision for both the Stage 2 artifact gate and
    OCR -- company policy is Azure CV as the only vision/OCR backend, no
    Tesseract) via the LangGraph orchestrator, then Shared Stages 6.5-10 when
    run_shared_publish=True, then the Stage 11 Cosmos publish when
    publish_to_cosmos=True. Cosmos publish stays opt-in per call since it
    writes the shared production corpus."""
    from orchestration.routing import extract_case_id

    run_id = f"run_incident_{case_id}_{uuid.uuid4().hex[:8]}"
    final_output_dir = Path(output_dir) if output_dir else (
        REPO_ROOT / "incidenceknowledgeingestion" / "data" / "output" / "incidents" / f"case_{case_id}"
    )

    detected_case_id = extract_case_id(Path(source_pdf_path).name)
    if detected_case_id != case_id:
        return {
            "run_id": run_id,
            "succeeded": False,
            "output_dir": str(final_output_dir),
            "review_status": "not_started",
            "stdout_tail": "",
            "stderr_tail": (
                f"source_pdf_path filename must encode case_id {case_id!r} (e.g. 'Case {case_id} Data.pdf') "
                f"-- the orchestrator this tool calls detects the case id from the filename, and detected "
                f"{detected_case_id!r} instead."
            ),
        }

    env = {**os.environ, "BRAIN_INGESTION_ENABLED": "1"}
    command = [
        sys.executable,
        str(REPO_ROOT / "orchestration" / "scripts" / "run_ingestion_agent.py"),
        "--source", source_pdf_path,
        "--output-dir", str(final_output_dir),
        "--source-stages", stages,
        "--ocr-backend", "azure_cv",
        "--json",
    ]
    if run_shared_publish:
        command.append("--with-publish")
    if publish_to_cosmos:
        command.extend(["--publish-to-cosmos", "--publish-scope", publish_scope])
    result = subprocess.run(command, env=env, capture_output=True, text=True)

    run_record = {
        "run_id": run_id,
        "pipeline": "incidence",
        "case_id": case_id,
        "output_dir": str(final_output_dir),
        "run_shared_publish": run_shared_publish,
        "publish_to_cosmos": publish_to_cosmos,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    }
    get_storage_provider().save_ingestion_run(run_record)

    return {
        "run_id": run_id,
        "succeeded": result.returncode == 0,
        "output_dir": str(final_output_dir),
        "review_status": "prepared_via_pipeline_hooks",
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:] if result.returncode != 0 else "",
    }


def tool_ingest_operational_source(
    source_pdf_path: str,
    source_id: str,
    source_type: str = "manual",
    output_dir: str | None = None,
    stages: str = "1,2,3,4,5,6,8",
    run_shared_publish: bool = False,
    publish_to_cosmos: bool = False,
    publish_scope: str = "all",
) -> dict[str, Any]:
    """One straight call covering the full operational pipeline: per-source
    Stages 1-8 (Azure Computer Vision OCR -- company policy is Azure CV as
    the only vision/OCR backend, no Tesseract) via the LangGraph
    orchestrator, then Shared Stages 6.5-10 when run_shared_publish=True,
    then the Stage 11 Cosmos publish when publish_to_cosmos=True. Cosmos
    publish stays opt-in per call since it writes the shared production
    corpus. `source_id` becomes the Brain scope
    "operational_sources/<source_id>" every stage hook writes into."""
    run_id = f"run_operational_{uuid.uuid4().hex[:8]}"
    final_output_dir = Path(output_dir) if output_dir else (
        REPO_ROOT / "operationalknowledgeingestion" / "data" / "output" / source_id
    )

    env = {**os.environ, "BRAIN_INGESTION_ENABLED": "1"}
    command = [
        sys.executable,
        str(REPO_ROOT / "orchestration" / "scripts" / "run_ingestion_agent.py"),
        "--source", source_pdf_path,
        "--source-id", source_id,
        "--output-dir", str(final_output_dir),
        "--source-stages", stages,
        "--ocr-backend", "azure_cv",
        "--json",
    ]
    if run_shared_publish:
        command.append("--with-publish")
    if publish_to_cosmos:
        command.extend(["--publish-to-cosmos", "--publish-scope", publish_scope])
    result = subprocess.run(command, env=env, capture_output=True, text=True)

    run_record = {
        "run_id": run_id,
        "pipeline": "operational",
        "source_pdf_path": source_pdf_path,
        "source_id": source_id,
        "output_dir": str(final_output_dir),
        "run_shared_publish": run_shared_publish,
        "publish_to_cosmos": publish_to_cosmos,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-4000:],
    }
    get_storage_provider().save_ingestion_run(run_record)

    return {
        "run_id": run_id,
        "succeeded": result.returncode == 0,
        "output_dir": str(final_output_dir),
        "review_status": "prepared_via_pipeline_hooks",
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:] if result.returncode != 0 else "",
    }
