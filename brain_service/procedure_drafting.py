"""Tool 8 -- draft_procedure. Drafts a Procedure FROM a Capability's own
populated fields (observables/sql_field_notes/support_contract/
when_to_use/role_paths/api_checks) plus retrieved Brain context, replacing
the old Stage 5/6 pipeline's reliance on the static
docs/ontology/catalogs/*.json snippets (shared_pipeline_stages/ontology_rag.py)
for procedure/runbook drafting -- see AGENT_DESIGN_NOTES.md §5/§5.1.

Follows the same two-phase shape as Tools 2-4: an LLM call proposes a
DraftedProcedure (types.py), then build_procedure_record() constructs and
validates a real brain.schemas.procedure.Procedure -- checking that every
referenced id (capability_id, allowed_role_entity_ids, per-step role ids)
actually exists in the corpus, mirroring persistence.py's
DanglingReferenceError discipline, since a Procedure drafted from
plausible-looking-but-nonexistent role ids would be exactly the same
silent-corruption bug found and fixed there for Relationships/Claims/
Capabilities.

Writing is a separate, explicit step (write_drafted_procedure) rather
than automatic -- unlike the four Create-path tools, a drafted Procedure
is not gated by an SME's Reconciliation decision on an existing corpus
delta; it is new content generation, so the review it produces is always
NEW_CANDIDATE, always OPERATIONAL_UNREVIEWED, and the caller decides
whether/when to call the write step (e.g. after inspecting `gaps`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from brain.id_generation import is_well_formed_id, procedure_id
from brain.schemas.capability import Capability
from brain.schemas.common import ValidationStatus
from brain.schemas.procedure import Procedure, ProcedureAction, ProcedureStep
from brain.schemas.review import ReviewKind
from brain_service.context import get_brain_context
from brain_service.review import build_review
from brain_service.types import DraftedProcedure
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "draft_procedure.md"


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


class CapabilityNotFoundError(ValueError):
    def __init__(self, capability_id: str) -> None:
        super().__init__(f"capability_id {capability_id!r} does not resolve to an existing Capability record")


def draft_procedure(
    llm: LLMProvider,
    storage: StorageProvider,
    *,
    capability_id: str,
    distinguishing_token: str,
    extra_source_evidence_ids: list[str] | None = None,
) -> DraftedProcedure:
    """`distinguishing_token` becomes part of the eventual Procedure's id
    (brain.id_generation.procedure_id) -- e.g. the incident case id or
    operational source id this drafting run is grounded in, since multiple
    Procedures may exist per Capability (schema docstring, §5.2)."""
    capability = _load_capability(storage, capability_id)

    seed_entity_ids = list(
        {
            *capability.target_entity_ids,
            *capability.allowed_surface_entity_ids,
            *capability.required_role_ids,
        }
    )
    context_packet = get_brain_context(
        storage,
        task={"tool": "draft_procedure", "capability_id": capability_id},
        entity_ids=seed_entity_ids or None,
        hops=1,
    )

    user_content = json.dumps(
        {
            "capability": capability.model_dump(mode="json"),
            "retrieved_context": context_packet.model_dump(mode="json"),
            "extra_source_evidence_ids": extra_source_evidence_ids or [],
        },
        ensure_ascii=False,
    )

    return llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=user_content,
        schema=DraftedProcedure,
        label="draft_procedure",
    )


def _load_capability(storage: StorageProvider, capability_id: str) -> Capability:
    # load_brain_context filters by entity_ids (Entity records only), not by
    # arbitrary record id, so a Capability lookup scans the corpus directly.
    for record in storage.load_brain_context():
        if isinstance(record, Capability) and record.id == capability_id:
            return record
    raise CapabilityNotFoundError(capability_id)


class DanglingProcedureReferenceError(ValueError):
    """Mirrors persistence.py's DanglingReferenceError -- a drafted
    Procedure referencing a role entity id that is well-formed but does
    not actually exist in the corpus must never write silently."""

    def __init__(self, dangling_ids: list[str]) -> None:
        self.dangling_ids = dangling_ids
        super().__init__(
            f"drafted Procedure references role entity id(s) not found in the corpus: {dangling_ids} -- "
            "create the referenced Entity/Entities first (as their own NEW_CANDIDATE)."
        )


def build_procedure_record(
    drafted: DraftedProcedure,
    storage: StorageProvider,
    *,
    capability_id: str,
    distinguishing_token: str,
    source_evidence_ids: list[str],
) -> Procedure:
    """Constructs and validates a real Procedure from the LLM's proposal.
    Raises CapabilityNotFoundError / DanglingProcedureReferenceError
    rather than writing a record with a dangling reference -- the same
    existence-check discipline persistence.py applies to NEW_CANDIDATE
    Relationships/Claims/Capabilities, extended here since draft_procedure
    is a second path (besides reconcile_candidate) that can introduce a
    new record into the corpus."""
    capability = _load_capability(storage, capability_id)

    existing_ids = {r.id for r in storage.load_brain_context()}
    referenced_role_ids = {
        *drafted.allowed_role_entity_ids,
        *[s.responsible_role_entity_id for s in drafted.steps if s.responsible_role_entity_id],
        *[s.supporting_role_entity_id for s in drafted.steps if s.supporting_role_entity_id],
        *[a.role_entity_id for s in drafted.steps for a in s.actions if a.role_entity_id],
    }
    dangling = sorted(rid for rid in referenced_role_ids if rid not in existing_ids)
    if dangling:
        raise DanglingProcedureReferenceError(dangling)

    steps = [
        ProcedureStep(
            step_number=step.step_number,
            title=step.title,
            instruction=step.instruction,
            responsible_role_entity_id=step.responsible_role_entity_id,
            supporting_role_entity_id=step.supporting_role_entity_id,
            purpose=step.purpose,
            expected_result=step.expected_result,
            healthy_condition=step.healthy_condition,
            failure_condition=step.failure_condition,
            stop_or_escalate_if=list(step.stop_or_escalate_if),
            actions=[
                ProcedureAction(label=a.label, exact_action=a.exact_action, role_entity_id=a.role_entity_id)
                for a in step.actions
            ],
            source_refs=list(step.source_refs) or list(source_evidence_ids),
        )
        for step in drafted.steps
    ]

    return Procedure(
        # capability_id is well-formed ("capability:<name>") -- strip the
        # type prefix before slugifying, matching the existing convention
        # in brain/migration/enrich_brain_knowledge.py's own procedure_id()
        # call, so a Procedure's id reads as "procedure:<name>:<token>"
        # rather than doubling the "capability_" prefix into the slug.
        id=procedure_id(capability_id.split(":", 1)[-1], distinguishing_token),
        capability_id=capability_id,
        procedure_type=capability.capability_kind,
        title=drafted.title,
        summary=drafted.summary,
        when_to_use=list(drafted.when_to_use),
        not_for=list(drafted.not_for),
        allowed_role_entity_ids=list(drafted.allowed_role_entity_ids),
        steps=steps,
        source_refs=list(source_evidence_ids),
        validation_status=ValidationStatus.OPERATIONAL_UNREVIEWED,
    )


def write_drafted_procedure(
    storage: StorageProvider,
    procedure: Procedure,
    *,
    scope: str,
) -> None:
    """Writes the drafted Procedure plus an auditable NEW_CANDIDATE review
    describing it -- matches apply_reconciliation's write-everything model
    (2026-09-09): the record lands immediately as OPERATIONAL_UNREVIEWED,
    the review is the audit trail an SME works from, not a gate blocking
    the write."""
    review = build_review(
        kind=ReviewKind.NEW_CANDIDATE,
        affected_record_ids=[procedure.id],
        proposed_change=(
            f"DRAFTED PROCEDURE for {procedure.capability_id}: {procedure.title!r} "
            f"({len(procedure.steps)} steps). Drafted from Brain-grounded context, not the "
            "static ontology catalog -- review steps against source_refs before approving."
        ),
        source_refs=procedure.source_refs,
    )
    storage.save_brain_records([procedure, review], scope=scope)
