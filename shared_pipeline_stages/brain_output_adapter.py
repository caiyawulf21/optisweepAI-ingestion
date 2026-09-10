"""Output-side adapter: turns shared Stage 7's canonical_runbooks.json and
shared Stage 8's canonical_playbooks.json entries into real, validated
Brain Procedure/Playbook records -- additive, alongside Stage 7/8's
existing JSON-file output, not a replacement for it. Stage 7/8's own
compatibility/scoring/confidence logic (link_scoring.py, normalize.py,
capability_derivation.py) is untouched; this module only runs AFTER that
logic has already produced its finalized dict, converting the result into
Brain's schema.

Follows the exact precedent brain/migration/enrich_brain_knowledge.py
already established for promoting a pre-Brain finalized runbook into a
real Procedure: wrap the whole source dict as ONE EvidenceUnit (its
`content.structured_payload` holds the dict verbatim), then every
Procedure/Playbook field derived from it cites that single EvidenceUnit's
id -- because canonical_runbooks.json/canonical_playbooks.json cite their
own provenance as free-form objects (source_document_id/page/quote, not
Brain evidence ids), there is no existing Brain EvidenceUnit for a step or
branch to cite directly, and inventing one id per citation object would
manufacture false precision this data doesn't actually have.

Role resolution (`_resolve_role`) and capability-tag resolution
(`_resolve_capability_id`) only ever return an id that ALREADY EXISTS in
the corpus -- never invented -- mirroring persistence.py's/
procedure_drafting.py's DanglingReferenceError discipline. A runbook/
playbook whose capability_tags or resolved_runbook_ids don't resolve to
anything already in Brain is not silently dropped or invented around: the
caller gets that back in the result's `gaps` list and decides what to do
(e.g. draft the missing Capability/Procedure first via draft_procedure).

Both entry points take a pre-built `BrainCorpusIndex` rather than a bare
`StorageProvider` -- a real caller adapts many runbooks/playbooks in one
run (Stage 7's canonical_runbooks.json alone holds ~270 entries), and each
of role/capability/procedure-id resolution needs a full corpus scan;
doing that scan once via `build_corpus_index()` rather than once per
adapted record is the difference between adapting the real corpus in
under a second and taking minutes (confirmed directly: the naive
per-record-storage.load_brain_context() version was still running after
two minutes against the real ~20K-record local corpus for 268 runbooks).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from brain.id_generation import entity_id, playbook_id, procedure_id, slugify
from brain.migration.capability_state_pairings import PAIRINGS
from brain.migration.common import content_hash
from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.common import ValidationStatus
from brain.schemas.entity import Entity, EntityType
from brain.schemas.evidence_unit import EvidenceContent, EvidenceKind, EvidenceUnit
from brain.schemas.playbook import BranchOutcome, Playbook, PlaybookBranch, PlaybookNode, PlaybookNodeType
from brain.schemas.procedure import Procedure, ProcedureAction, ProcedureStep
from providers.storage import StorageProvider

_NODE_TYPE_ALIASES = {
    # canonical_playbooks.json node_type values not already valid
    # PlaybookNodeType members -- mapped to their closest Brain equivalent
    # rather than left to raise, since Stage 8's own vocabulary
    # (branching_condition) predates Brain's node-type enum.
    "branching_condition": PlaybookNodeType.DIAGNOSTIC_DECISION,
}


@dataclass(frozen=True)
class BrainCorpusIndex:
    """Pre-computed lookups built once from a full corpus scan, reused
    across every runbook/playbook adapted in one run -- see the module
    docstring's note on why this matters (a per-record scan against the
    real ~20K-record corpus does not finish in reasonable time across
    ~270 runbooks). Immutable and cheap to pass around; rebuild only when
    the corpus has actually changed (e.g. after writing newly-promoted
    Procedures, if a caller wants those visible for canonical_playbook_to_playbook's
    procedure-id resolution within the same run)."""

    role_ids_by_slug: dict[str, str]
    capability_ids: set[str]
    entity_ids: set[str]
    procedure_id_by_original_id: dict[str, str]


def build_corpus_index(storage: StorageProvider) -> BrainCorpusIndex:
    """The one full-corpus scan this module needs -- call once per batch
    (or once more after writing newly-promoted records, if a caller needs
    canonical_playbook_to_playbook to see Procedures promoted earlier in
    the same run)."""
    role_ids_by_slug: dict[str, str] = {}
    capability_ids: set[str] = set()
    entity_ids: set[str] = set()
    evidence_by_id: dict[str, EvidenceUnit] = {}
    procedures: list[Procedure] = []

    for record in storage.load_brain_context():
        if isinstance(record, Entity):
            entity_ids.add(record.id)
            if record.entity_type == EntityType.ROLE:
                role_ids_by_slug[slugify(record.name)] = record.id
        elif isinstance(record, Capability):
            capability_ids.add(record.id)
        elif isinstance(record, EvidenceUnit):
            evidence_by_id[record.id] = record
        elif isinstance(record, Procedure):
            procedures.append(record)

    procedure_id_by_original_id: dict[str, str] = {}
    for proc in procedures:
        for ref in proc.source_refs:
            evidence = evidence_by_id.get(ref)
            if evidence is None or not evidence.content.structured_payload:
                continue
            original_id = evidence.content.structured_payload.get("procedure_id")
            if original_id:
                procedure_id_by_original_id[str(original_id)] = proc.id

    return BrainCorpusIndex(
        role_ids_by_slug=role_ids_by_slug,
        capability_ids=capability_ids,
        entity_ids=entity_ids,
        procedure_id_by_original_id=procedure_id_by_original_id,
    )


def _resolve_role(role_name: Any, *, index: BrainCorpusIndex) -> str | None:
    """Matches a plain role string (e.g. "operator", "L1_support") to an
    ALREADY-EXISTING entity:role:* id -- never constructs/writes a new
    Entity."""
    if not role_name or not str(role_name).strip():
        return None
    return index.role_ids_by_slug.get(slugify(str(role_name)))


def _resolve_capability_id(tag: Any, *, index: BrainCorpusIndex) -> str | None:
    """Matches a capability_tags[] entry to an already-existing Brain
    Capability id -- never invents one. capability_tags[] uses the
    PRE-RENAME catalog slug (e.g. "device_roster_state"), while Brain's
    real Capability ids use the renamed convention from the backfill
    (e.g. "capability:confirm_device_roster_state") -- confirmed by
    comparing real corpus data directly (zero of the first 60 real
    runbooks resolved under a naive direct-slug guess). Reuses the exact
    three-step resolution (direct id, PAIRINGS lookup, fuzzy suffix match)
    brain/migration/enrich_brain_knowledge.py::_catalog_slug_to_capability_id
    already established and validated for this identical problem, rather
    than re-deriving a second, possibly-divergent mapping."""
    if not tag or not str(tag).strip():
        return None
    slug = str(tag).strip()
    direct = f"capability:{slugify(slug)}"
    if direct in index.capability_ids:
        return direct
    pairing = PAIRINGS.get(slug)
    if pairing:
        renamed = f"capability:{slugify(pairing['new_capability_id_suffix'])}"
        if renamed in index.capability_ids:
            return renamed
    needle = slugify(slug)
    for cap_id in index.capability_ids:
        suffix = cap_id.split(":", 1)[-1]
        if suffix == needle or suffix.endswith("_" + needle) or needle in suffix:
            return cap_id
    return None


@dataclass
class AdaptedProcedureResult:
    evidence: EvidenceUnit
    procedure: Procedure | None
    gaps: list[str] = field(default_factory=list)


def canonical_runbook_to_procedure(
    runbook: dict[str, Any],
    *,
    index: BrainCorpusIndex,
    source_id: str,
) -> AdaptedProcedureResult:
    """Wraps `runbook` (one entry from canonical_runbooks.json's
    "runbooks" list) as an EvidenceUnit, then builds a Procedure from it
    if -- and only if -- at least one of its capability_tags resolves to
    an existing Brain Capability (a Procedure with no capability_id would
    fail Procedure's own well-formed-capability-id validator, and there is
    no capability to invent one for). When no tag resolves, returns the
    wrapping EvidenceUnit alone plus a `gaps` entry naming what's missing
    -- the caller can draft the missing Capability first (draft_procedure
    assumes a Capability already exists) rather than this adapter silently
    fabricating one.

    `index` comes from build_corpus_index() -- built once per batch, not
    once per runbook (see module docstring).
    """
    gaps: list[str] = []
    procedure_id_raw = str(runbook.get("procedure_id") or "")
    evidence = _wrap_as_evidence(
        runbook,
        source_id=source_id,
        evidence_kind_hint=f"canonical_runbook:{procedure_id_raw or 'unknown'}",
    )

    resolved_capability_id = None
    for tag in runbook.get("capability_tags") or []:
        resolved_capability_id = _resolve_capability_id(tag, index=index)
        if resolved_capability_id:
            break
    if resolved_capability_id is None:
        gaps.append(
            f"no capability_tags entry for runbook {procedure_id_raw!r} resolves to an existing "
            f"Brain Capability (tags seen: {runbook.get('capability_tags')!r}) -- "
            "draft/create that Capability first."
        )
        return AdaptedProcedureResult(evidence=evidence, procedure=None, gaps=gaps)

    role_ids: list[str] = []
    for role_name in (
        runbook.get("role_required"),
        runbook.get("responsible_role"),
        *(runbook.get("supporting_roles") or []),
        *(runbook.get("audience_roles") or []),
    ):
        rid = _resolve_role(role_name, index=index)
        if rid and rid not in role_ids:
            role_ids.append(rid)
        elif role_name and not rid:
            gaps.append(f"role {role_name!r} on runbook {procedure_id_raw!r} has no matching entity:role:* in Brain")

    procedure_kind = _normalize_procedure_kind(runbook.get("procedure_type"))

    steps: list[ProcedureStep] = []
    for idx, raw_step in enumerate(runbook.get("steps") or [], start=1):
        if not isinstance(raw_step, dict):
            continue
        responsible = _resolve_role(raw_step.get("responsible_role"), index=index)
        supporting = _resolve_role(raw_step.get("supporting_role"), index=index)
        actions = [
            ProcedureAction(
                label=str(action.get("label") or action.get("action_type") or "action")[:200],
                exact_action=str(action.get("exact_action") or ""),
                role_entity_id=_resolve_role(action.get("role_required"), index=index),
            )
            for action in raw_step.get("actions") or []
            if isinstance(action, dict) and str(action.get("exact_action") or "").strip()
        ]
        stop_if = raw_step.get("stop_or_escalate_if") or []
        if isinstance(stop_if, str):
            stop_if = [stop_if]
        steps.append(
            ProcedureStep(
                step_number=idx,
                title=str(raw_step.get("title") or f"Step {idx}")[:300],
                instruction=str(raw_step.get("instruction") or raw_step.get("title") or "")[:4000],
                responsible_role_entity_id=responsible,
                supporting_role_entity_id=supporting,
                purpose=str(raw_step.get("purpose") or ""),
                expected_result=str(raw_step.get("expected_result") or ""),
                healthy_condition=str(raw_step.get("healthy_condition") or ""),
                failure_condition=str(raw_step.get("failure_condition") or ""),
                stop_or_escalate_if=[str(s) for s in stop_if if s],
                actions=actions,
                source_refs=[evidence.id],
            )
        )

    if not steps:
        gaps.append(f"runbook {procedure_id_raw!r} has no usable steps -- skipping Procedure construction")
        return AdaptedProcedureResult(evidence=evidence, procedure=None, gaps=gaps)

    procedure = Procedure(
        id=procedure_id(resolved_capability_id.split(":", 1)[-1], f"{source_id}_{slugify(procedure_id_raw)[:80]}"),
        capability_id=resolved_capability_id,
        procedure_type=procedure_kind,
        title=str(runbook.get("title") or ""),
        summary=str(runbook.get("summary") or ""),
        when_to_use=_as_str_list(runbook.get("when_to_use")),
        not_for=_as_str_list(runbook.get("not_for")),
        allowed_role_entity_ids=role_ids,
        steps=steps,
        source_refs=[evidence.id],
        validation_status=ValidationStatus.OPERATIONAL_UNREVIEWED,
    )
    return AdaptedProcedureResult(evidence=evidence, procedure=procedure, gaps=gaps)


@dataclass
class AdaptedPlaybookResult:
    evidence: EvidenceUnit
    playbook: Playbook | None
    gaps: list[str] = field(default_factory=list)


def canonical_playbook_to_playbook(
    playbook: dict[str, Any],
    *,
    index: BrainCorpusIndex,
    source_id: str,
) -> AdaptedPlaybookResult:
    """Wraps `playbook` (one entry from canonical_playbooks.json's
    "playbooks" list) as an EvidenceUnit, then builds a Playbook from it.
    A node's `resolved_runbook_ids`/`linked_primary_procedure` values are
    Stage 7's own "proc_*_v1"-style ids, which only resolve to a real
    Brain procedure:* id if that exact runbook was already promoted via
    canonical_runbook_to_procedure() in this same corpus -- resolved via
    `index.procedure_id_by_original_id`. A node whose linked runbook(s)
    haven't been promoted yet becomes a `diagnostic_decision` node instead
    of `procedure_reference` (never a procedure_reference node with a
    fabricated procedure_id, which Procedure's own validator would accept
    as well-formed-looking but Brain has no way to verify actually
    exists) and the gap is named in the result, not silently dropped.

    `index` comes from build_corpus_index() -- rebuild it after writing
    newly-promoted Procedures earlier in the same run if this playbook's
    nodes should see them (see build_corpus_index's own docstring).
    """
    gaps: list[str] = []
    playbook_id_raw = str(playbook.get("playbook_id") or playbook.get("playbook_candidate_id") or "")
    evidence = _wrap_as_evidence(
        playbook,
        source_id=source_id,
        evidence_kind_hint=f"canonical_playbook:{playbook_id_raw or 'unknown'}",
    )

    nodes: list[PlaybookNode] = []
    for raw_node in playbook.get("nodes") or []:
        if not isinstance(raw_node, dict):
            continue
        node_id = str(raw_node.get("node_id") or "")
        raw_node_type = str(raw_node.get("node_type") or "diagnostic_decision")
        node_type = _NODE_TYPE_ALIASES.get(raw_node_type)
        if node_type is None:
            try:
                node_type = PlaybookNodeType(raw_node_type)
            except ValueError:
                node_type = PlaybookNodeType.DIAGNOSTIC_DECISION

        resolved_procedure_id = None
        candidate_runbook_ids = [
            raw_node.get("linked_primary_procedure"),
            *(raw_node.get("resolved_runbook_ids") or []),
        ]
        for candidate in candidate_runbook_ids:
            if candidate and str(candidate) in index.procedure_id_by_original_id:
                resolved_procedure_id = index.procedure_id_by_original_id[str(candidate)]
                break
        if candidate_runbook_ids and any(candidate_runbook_ids) and resolved_procedure_id is None:
            gaps.append(
                f"node {node_id!r} links runbook id(s) {candidate_runbook_ids!r} that have not been "
                "promoted to a Brain Procedure yet -- run canonical_runbook_to_procedure for that "
                "runbook first, or leave this node as diagnostic_decision."
            )
        if node_type == PlaybookNodeType.PROCEDURE_REFERENCE and resolved_procedure_id is None:
            # Never emit a procedure_reference node with no real procedure_id
            # -- Procedure's own schema requires one for this node type.
            node_type = PlaybookNodeType.DIAGNOSTIC_DECISION

        allowed_role_ids = [
            rid
            for role_name in (raw_node.get("allowed_roles") or raw_node.get("preferred_audience") or [])
            if (rid := _resolve_role(role_name, index=index))
        ]

        branches: list[PlaybookBranch] = []
        for raw_branch in raw_node.get("branches") or []:
            if not isinstance(raw_branch, dict):
                continue
            outcome = _normalize_branch_outcome(raw_branch.get("outcome"))
            if outcome is None:
                gaps.append(f"node {node_id!r} branch {raw_branch.get('branch_id')!r} has unrecognized outcome, skipped")
                continue
            branches.append(
                PlaybookBranch(
                    outcome=outcome,
                    condition=str(raw_branch.get("condition_descriptor") or raw_branch.get("condition_label") or ""),
                    next_node_id=str(raw_branch.get("next_node_id")) if raw_branch.get("next_node_id") else None,
                    source_refs=[evidence.id],
                )
            )

        nodes.append(
            PlaybookNode(
                node_id=node_id,
                node_order=int(raw_node.get("node_order") or len(nodes) + 1),
                node_type=node_type,
                title=str(raw_node.get("title") or ""),
                capability_id=None,
                procedure_id=resolved_procedure_id,
                symptom_entity_id=None,
                intent=str(raw_node.get("intent") or raw_node.get("goal") or ""),
                allowed_role_entity_ids=allowed_role_ids,
                stop_or_escalation_note=str(raw_node.get("stop_or_escalation_note") or ""),
                branches=branches,
                source_refs=[evidence.id],
            )
        )

    if not nodes:
        gaps.append(f"playbook {playbook_id_raw!r} has no usable nodes -- skipping Playbook construction")
        return AdaptedPlaybookResult(evidence=evidence, playbook=None, gaps=gaps)

    node_ids = {n.node_id for n in nodes}
    # Drop next_node_id targets that don't resolve within this same
    # playbook rather than letting Playbook's own validator hard-fail the
    # whole record over one dangling branch target from source data this
    # adapter doesn't control.
    for node in nodes:
        for i, branch in enumerate(node.branches):
            if branch.next_node_id is not None and branch.next_node_id not in node_ids:
                gaps.append(
                    f"node {node.node_id!r} branch targets {branch.next_node_id!r}, "
                    "which is not a node in this playbook -- branch target cleared"
                )
                node.branches[i] = branch.model_copy(update={"next_node_id": None})

    entry_symptom_ids = [
        eid
        for eid in ([playbook.get("entry_symptom_entity_id")] if playbook.get("entry_symptom_entity_id") else [])
        if eid in index.entity_ids
    ]

    try:
        result = Playbook(
            id=playbook_id(f"{source_id}_{slugify(playbook_id_raw)[:80]}"),
            title=str(playbook.get("title") or ""),
            playbook_goal=str(playbook.get("playbook_goal") or playbook.get("user_facing_summary") or ""),
            entry_symptom_entity_ids=entry_symptom_ids,
            affected_entity_ids=[],
            nodes=nodes,
            entry_node_id=nodes[0].node_id,
            confidence=str(playbook.get("confidence") or "needs_review"),
            source_refs=[evidence.id],
            validation_status=ValidationStatus.OPERATIONAL_UNREVIEWED,
        )
    except ValueError as exc:
        gaps.append(f"playbook {playbook_id_raw!r} failed schema validation after adaptation: {exc}")
        return AdaptedPlaybookResult(evidence=evidence, playbook=None, gaps=gaps)

    return AdaptedPlaybookResult(evidence=evidence, playbook=result, gaps=gaps)


def _wrap_as_evidence(payload: dict[str, Any], *, source_id: str, evidence_kind_hint: str) -> EvidenceUnit:
    import json

    text_summary = str(payload.get("summary") or payload.get("title") or payload.get("playbook_goal") or "")
    return EvidenceUnit(
        id=f"evidence:{source_id}:{slugify(evidence_kind_hint)[:120]}",
        evidence_kind=EvidenceKind.DOCUMENT_SECTION,
        source_type="shared_pipeline_output",
        source_id=source_id,
        content=EvidenceContent(
            text=text_summary or evidence_kind_hint,
            is_verbatim=False,
            content_hash=content_hash(evidence_kind_hint, json.dumps(payload, sort_keys=True, default=str)),
            structured_payload=payload,
        ),
    )


def _as_str_list(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _normalize_procedure_kind(value: Any) -> CapabilityKind:
    if isinstance(value, str):
        normalized = value.strip().lower()
        for member in CapabilityKind:
            if member.value == normalized:
                return member
    return CapabilityKind.DIAGNOSTIC


def _normalize_branch_outcome(value: Any) -> BranchOutcome | None:
    if not value:
        return None
    normalized = str(value).strip().lower()
    for member in BranchOutcome:
        if member.value == normalized:
            return member
    return None
