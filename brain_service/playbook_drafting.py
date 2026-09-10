"""Tool 9 -- draft_playbook. Drafts symptom-driven branching logic FROM
Brain's own graph (symptom Entities -> MAY_INDICATE/VERIFIES/CAUSES/
CONTRIBUTES_TO -> Capabilities -> their already-drafted Procedures),
replacing the old Stage 8 pipeline's playbook finalization
(shared_pipeline_stages/stage_8/) for the same reason draft_procedure
replaces Stage 5/6's static-catalog drafting -- see AGENT_DESIGN_NOTES.md
§5/§5.1/§5.2 ("runbooks are not incident-only": a playbook must draw on
the full corpus of already-approved Procedures, not just one incident).

Deliberately sequenced AFTER draft_procedure (Tool 8): a Playbook's
`procedure_reference` nodes must cite real, already-existing procedure_id
values -- it never drafts new Procedure content itself, matching the
schema's own docstring ("A Playbook never embeds a Procedure's steps").

Follows the same two-phase shape as draft_procedure: an LLM call proposes
a DraftedPlaybook (types.py), then build_playbook_record() constructs and
validates a real brain.schemas.playbook.Playbook -- checking that every
referenced id (capability_id, procedure_id, symptom_entity_id, role ids)
actually exists in the corpus, mirroring persistence.py's/
procedure_drafting.py's DanglingReferenceError discipline.
"""

from __future__ import annotations

import json
from pathlib import Path

from brain.id_generation import playbook_id
from brain.schemas.capability import Capability
from brain.schemas.common import ValidationStatus
from brain.schemas.entity import Entity
from brain.schemas.playbook import BranchOutcome, Playbook, PlaybookBranch, PlaybookNode, PlaybookNodeType
from brain.schemas.procedure import Procedure
from brain.schemas.relationship import Relationship, RelationshipType
from brain.schemas.review import ReviewKind
from brain_service.context import get_brain_context
from brain_service.review import build_review
from brain_service.types import DraftedPlaybook
from providers.llm import LLMProvider
from providers.storage import StorageProvider

_PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "draft_playbook.md"

_SYMPTOM_TRAVERSAL_TYPES = [
    RelationshipType.MAY_INDICATE,
    RelationshipType.VERIFIES,
    RelationshipType.CAUSES,
    RelationshipType.CONTRIBUTES_TO,
]


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


class SymptomNotFoundError(ValueError):
    def __init__(self, entity_id: str) -> None:
        super().__init__(f"entry symptom entity id {entity_id!r} does not resolve to an existing Entity record")


def draft_playbook(
    llm: LLMProvider,
    storage: StorageProvider,
    *,
    entry_symptom_entity_ids: list[str],
    distinguishing_token: str,
) -> DraftedPlaybook:
    """`distinguishing_token` becomes part of the eventual Playbook's id
    (brain.id_generation.playbook_id) -- e.g. a symptom cluster name or
    incident case id this drafting run is grounded in."""
    existing_entity_ids = {
        r.id for r in storage.load_brain_context(entity_ids=entry_symptom_entity_ids) if isinstance(r, Entity)
    }
    for entity_id in entry_symptom_entity_ids:
        if entity_id not in existing_entity_ids:
            raise SymptomNotFoundError(entity_id)

    # get_brain_context's traversal reaches connected Entities via
    # Relationships (symptom -MAY_INDICATE-> capability is itself an
    # Entity<->Entity-shaped edge at the graph level -- Capability ids are
    # just another well-formed id a Relationship endpoint can hold), but it
    # never resolves into Capability/Procedure record CONTENT -- ContextPacket
    # only ever carries entity/evidence ids (context_packet.py's own
    # docstring). draft_procedure hit this same gap and solved it the same
    # way: explicitly load the full records the traversal's ids point at,
    # rather than only forwarding bare ids to the LLM.
    context_packet = get_brain_context(
        storage,
        task={"tool": "draft_playbook", "entry_symptom_entity_ids": entry_symptom_entity_ids},
        entity_ids=entry_symptom_entity_ids,
        relationship_types=_SYMPTOM_TRAVERSAL_TYPES,
        hops=2,
    )

    all_records = storage.load_brain_context()
    relationships = [
        r
        for r in all_records
        if isinstance(r, Relationship)
        and r.relationship_type in _SYMPTOM_TRAVERSAL_TYPES
        and (r.from_id in entry_symptom_entity_ids or r.to_id in entry_symptom_entity_ids)
    ]
    reachable_capability_ids = sorted(
        {r.to_id for r in relationships if r.to_id.startswith("capability:")}
        | {r.from_id for r in relationships if r.from_id.startswith("capability:")}
    )
    capabilities = [r for r in all_records if isinstance(r, Capability) and r.id in reachable_capability_ids]
    existing_procedures = [
        {"procedure_id": p.id, "capability_id": p.capability_id, "title": p.title, "summary": p.summary}
        for p in all_records
        if isinstance(p, Procedure) and p.capability_id in reachable_capability_ids
    ]

    user_content = json.dumps(
        {
            "entry_symptom_entity_ids": entry_symptom_entity_ids,
            "retrieved_context": context_packet.model_dump(mode="json"),
            "symptom_relationships": [
                {
                    "from_id": r.from_id,
                    "relationship_type": r.relationship_type.value,
                    "to_id": r.to_id,
                    "note": r.note,
                }
                for r in relationships
            ],
            "reachable_capabilities": [c.model_dump(mode="json") for c in capabilities],
            "existing_procedures_for_reachable_capabilities": existing_procedures,
        },
        ensure_ascii=False,
    )

    return llm.generate_json(
        system_prompt=_load_prompt(),
        user_content=user_content,
        schema=DraftedPlaybook,
        label="draft_playbook",
    )


class DanglingPlaybookReferenceError(ValueError):
    """Mirrors procedure_drafting.DanglingProcedureReferenceError -- a
    drafted Playbook node referencing a capability_id/procedure_id/
    symptom_entity_id/role id that is well-formed but does not actually
    exist in the corpus must never write silently. A dangling
    procedure_id is the highest-value check here specifically: the whole
    point of a Playbook is to route to a REAL, already-vetted Procedure,
    never an invented one."""

    def __init__(self, dangling_ids: list[str]) -> None:
        self.dangling_ids = dangling_ids
        super().__init__(
            f"drafted Playbook references id(s) not found in the corpus: {dangling_ids} -- "
            "a Playbook must only reference existing Capabilities/Procedures/Entities, never invent one."
        )


def build_playbook_record(
    drafted: DraftedPlaybook,
    storage: StorageProvider,
    *,
    distinguishing_token: str,
    source_evidence_ids: list[str],
) -> Playbook:
    """Constructs and validates a real Playbook from the LLM's proposal.
    Raises DanglingPlaybookReferenceError rather than writing a record
    with a dangling reference -- extending the same existence-check
    discipline procedure_drafting.py applies, since a Playbook has three
    separate kinds of reference (capability_id, procedure_id,
    symptom_entity_id) any of which could be a plausible-looking invention
    if left unchecked. brain.schemas.playbook.Playbook's own validators
    already catch a malformed id SHAPE and unresolvable branch targets
    WITHIN the playbook -- this adds the existence-in-corpus check those
    validators cannot perform on their own (they have no storage access)."""
    existing_ids = {r.id for r in storage.load_brain_context()}

    referenced_ids: set[str] = set(drafted.entry_symptom_entity_ids) | set(drafted.affected_entity_ids)
    for node in drafted.nodes:
        for value in (node.capability_id, node.procedure_id, node.symptom_entity_id):
            if value:
                referenced_ids.add(value)
        referenced_ids.update(node.allowed_role_entity_ids)

    dangling = sorted(rid for rid in referenced_ids if rid not in existing_ids)
    if dangling:
        raise DanglingPlaybookReferenceError(dangling)

    nodes = [
        PlaybookNode(
            node_id=node.node_id,
            node_order=node.node_order,
            node_type=PlaybookNodeType(node.node_type),
            title=node.title,
            capability_id=node.capability_id,
            procedure_id=node.procedure_id,
            symptom_entity_id=node.symptom_entity_id,
            intent=node.intent,
            allowed_role_entity_ids=list(node.allowed_role_entity_ids),
            stop_or_escalation_note=node.stop_or_escalation_note,
            branches=[
                PlaybookBranch(
                    outcome=BranchOutcome(branch.outcome),
                    condition=branch.condition,
                    next_node_id=branch.next_node_id,
                    source_refs=list(branch.source_refs) or list(source_evidence_ids),
                )
                for branch in node.branches
            ],
            source_refs=list(node.source_refs) or list(source_evidence_ids),
        )
        for node in drafted.nodes
    ]

    return Playbook(
        id=playbook_id(distinguishing_token),
        title=drafted.title,
        playbook_goal=drafted.playbook_goal,
        entry_symptom_entity_ids=list(drafted.entry_symptom_entity_ids),
        affected_entity_ids=list(drafted.affected_entity_ids),
        nodes=nodes,
        entry_node_id=drafted.entry_node_id,
        confidence=drafted.confidence,
        source_refs=list(source_evidence_ids),
        validation_status=ValidationStatus.OPERATIONAL_UNREVIEWED,
    )


def write_drafted_playbook(
    storage: StorageProvider,
    playbook: Playbook,
    *,
    scope: str,
) -> None:
    """Writes the drafted Playbook plus an auditable NEW_CANDIDATE review
    describing it -- matches write_drafted_procedure's model exactly."""
    review = build_review(
        kind=ReviewKind.NEW_CANDIDATE,
        affected_record_ids=[playbook.id],
        proposed_change=(
            f"DRAFTED PLAYBOOK {playbook.title!r} ({len(playbook.nodes)} nodes) for entry symptoms "
            f"{playbook.entry_symptom_entity_ids}. Drafted from Brain-grounded context (symptom graph "
            "traversal + existing Procedures), not the static ontology catalog -- review branch "
            "conditions and procedure_id references against source_refs before approving."
        ),
        source_refs=playbook.source_refs,
    )
    storage.save_brain_records([playbook, review], scope=scope)
