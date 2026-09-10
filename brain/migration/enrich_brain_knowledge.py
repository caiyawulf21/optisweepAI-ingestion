"""Enrich the local Brain corpus from ontology catalogs + operational runbooks.

Acts as the offline "knowledge enrichment" pass a future ingestion agent
should replicate (see brain/AGENT_DESIGN_NOTES.md §7):

1. Restore Capability.role_paths text lost when Pass 0 kept only role IDs.
2. Fill SqlFieldNote.database_entity_id from table payload / catalog DB slug.
3. Promote finalized-runbook EvidenceUnit.structured_payload into Procedure
   records (steps, actions including exact SQL, role entity IDs).
4. Add Claim records for per-role guidance and for grounded SELECT statements.
5. Link each new Procedure to its Capability with Relationship(USES).

Never invents SQL, role policy, or steps that are not present in catalog or
runbook evidence. Re-runnable; IDs are content-derived.

Run:
  python -m brain.migration.enrich_brain_knowledge
  python -m brain.migration.enrich_brain_knowledge --write
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from brain.id_generation import (
    capability_id,
    claim_id,
    entity_id,
    procedure_id,
    relationship_id,
    slugify,
)
from brain.migration.capability_state_pairings import PAIRINGS
from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.merge import merge_list_field, merge_record
from brain.schemas.capability import Capability, RolePathGuidance, SqlFieldNote
from brain.schemas.claim import Claim, LiteralValueObject, Polarity
from brain.schemas.common import utc_now
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.procedure import Procedure, ProcedureAction, ProcedureStep
from brain.schemas.relationship import Relationship, RelationshipType
from brain.validators import validate_batch
CATALOGS_DIR = REPO_ROOT / "docs" / "ontology" / "catalogs"
LOCAL_DIR = REPO_ROOT / "brain" / "data" / "local"
ONTOLOGY_DIR = LOCAL_DIR / "ontology_catalogs"
OPERATIONAL_DIR = LOCAL_DIR / "operational_sources"

# Extra alias tags seen on Stage 6 runbooks that are not PAIRINGS keys.
TAG_ALIASES: dict[str, str] = {}

SELECT_RE = re.compile(
    r"(SELECT\s+.+?)(?:;|\n\n|$)",
    re.IGNORECASE | re.DOTALL,
)
FROM_TABLE_RE = re.compile(
    r"FROM\s+(?:\[[^\]]+\]\.)?(?:\[dbo\]\.)?\[?([A-Za-z0-9_]+)\]?",
    re.IGNORECASE,
)


def _now():
    return utc_now()


def _load_records(path: Path, model):
    if not path.exists():
        return []
    return [model.model_validate(item) for item in load_json(path)]


def _wcs_sql_entity_id(entities_by_id: dict[str, Entity]) -> str | None:
    direct = entity_id("system", "wcs_sql")
    if direct in entities_by_id:
        return direct
    for eid, ent in entities_by_id.items():
        if ent.entity_type.value == "system" and slugify(ent.name) == "wcs_sql":
            return eid
    return None


def _catalog_slug_to_capability_id(slug: str, capabilities: dict[str, Capability]) -> str | None:
    """Map a pre-rename catalog/runbook capability tag to a live Brain capability id."""
    if not slug:
        return None
    slug = str(slug).strip()
    slug = TAG_ALIASES.get(slug, slug)
    direct = capability_id(slug)
    if direct in capabilities:
        return direct
    pairing = PAIRINGS.get(slug)
    if pairing:
        renamed = capability_id(pairing["new_capability_id_suffix"])
        if renamed in capabilities:
            return renamed
    needle = slugify(slug)
    for cap_id in capabilities:
        suffix = cap_id.split(":", 1)[-1]
        if suffix == needle or suffix.endswith("_" + needle) or needle in suffix:
            return cap_id
    return None

def _role_entity_id(role_name: str, entities_by_id: dict[str, Entity]) -> str | None:
    if not role_name or not str(role_name).strip():
        return None
    raw = str(role_name).strip()
    candidates = [
        entity_id("role", raw),
        entity_id("role", raw.replace(" ", "_")),
        entity_id("role", slugify(raw)),
    ]
    # Catalog uses L1_support; brain may have entity:role:l1_support
    lowered = slugify(raw)
    for eid, ent in entities_by_id.items():
        if ent.entity_type.value != "role":
            continue
        if eid in candidates or slugify(ent.name) == lowered:
            return eid
        if any(slugify(a) == lowered for a in ent.aliases):
            return eid
    return entity_id("role", lowered) if any(e.id == entity_id("role", lowered) for e in entities_by_id.values()) else None


def _resolve_role(role_name: str, entities_by_id: dict[str, Entity]) -> str | None:
    found = _role_entity_id(role_name, entities_by_id)
    if found and found in entities_by_id:
        return found
    # Try common normalizations
    for alt in (
        role_name,
        role_name.lower(),
        role_name.replace("-", "_"),
        "l2_support" if role_name.lower() in {"l2", "l2 support"} else None,
        "l1_support" if role_name.lower() in {"l1", "l1 support"} else None,
        "l3_support" if role_name.lower() in {"l3", "l3 support"} else None,
        "operator" if "operator" in role_name.lower() else None,
    ):
        if not alt:
            continue
        eid = entity_id("role", slugify(alt))
        if eid in entities_by_id:
            return eid
    return None


def _database_id_for_table(
    table_entity_id: str | None,
    entities_by_id: dict[str, Entity],
    db_name_to_id: dict[str, str],
) -> str | None:
    if not table_entity_id:
        return None
    table = entities_by_id.get(table_entity_id)
    if table is None:
        return None
    payload = table.payload
    db_name = getattr(payload, "database_name", None)
    if not db_name:
        return None
    return db_name_to_id.get(slugify(db_name)) or db_name_to_id.get(db_name.lower())


def _build_db_name_index(entities: list[Entity]) -> dict[str, str]:
    index: dict[str, str] = {}
    for ent in entities:
        if ent.entity_type.value != "database":
            continue
        index[slugify(ent.name)] = ent.id
        index[ent.name.lower()] = ent.id
        for alias in ent.aliases:
            index[slugify(alias)] = ent.id
            index[alias.lower()] = ent.id
            # Helix2x_*_Robotics → robotics
            if "_" in alias:
                tail = alias.split("_")[-1]
                index[slugify(tail)] = ent.id
    return index


def _table_name_index(entities: list[Entity]) -> dict[str, str]:
    index: dict[str, str] = {}
    for ent in entities:
        if ent.entity_type.value != "database_table":
            continue
        index[slugify(ent.name)] = ent.id
        index[ent.name.lower()] = ent.id
        for alias in ent.aliases:
            index[slugify(alias)] = ent.id
    return index


def enrich_capabilities_from_catalog(
    capabilities: dict[str, Capability],
    entities_by_id: dict[str, Entity],
    db_name_to_id: dict[str, str],
) -> tuple[dict[str, Capability], list[Claim], dict[str, int]]:
    stats = defaultdict(int)
    new_claims: list[Claim] = []
    catalog = load_json(CATALOGS_DIR / "capability_catalog.json")
    catalog_evidence_by_slug: dict[str, list[str]] = {}

    # Prefer existing catalog evidence units already in Brain for provenance.
    for cap in catalog.get("capabilities", []):
        old_slug = cap["id"]
        cap_id = _catalog_slug_to_capability_id(old_slug, capabilities)
        if cap_id is None:
            stats["catalog_cap_unmapped"] += 1
            continue
        current = capabilities[cap_id]
        source_refs = list(current.source_refs) or [
            f"evidence:catalog_capabilities_{slugify(old_slug)}_job"
        ]
        catalog_evidence_by_slug[old_slug] = source_refs

        role_paths: list[RolePathGuidance] = []
        for role_name, guidance in (cap.get("role_paths") or {}).items():
            if not isinstance(guidance, str) or not guidance.strip():
                continue
            role_id = _resolve_role(role_name, entities_by_id)
            if role_id is None:
                stats["role_unresolved"] += 1
                continue
            role_paths.append(RolePathGuidance(role_entity_id=role_id, guidance=guidance.strip()))
            claim = Claim(
                id=claim_id(slugify(role_id), f"role_path_{slugify(cap_id)}"),
                subject_entity_id=role_id,
                predicate="role_path_guidance",
                object=LiteralValueObject(value=guidance.strip()),
                polarity=Polarity.AFFIRMED,
                condition=cap_id,
                note=f"Per-role guidance for {current.name} (from ontology capability catalog).",
                source_refs=source_refs[:1],
                created_at=_now(),
                updated_at=_now(),
            )
            new_claims.append(claim)
            stats["role_path_claims"] += 1

        # Rebuild sql notes with database_entity_id; grow-richer merge later.
        sql_notes: list[SqlFieldNote] = []
        for link in cap.get("sql_model_links", []):
            db_name = link.get("database") or ""
            db_id = db_name_to_id.get(slugify(db_name)) if db_name else None
            table_id = entity_id("database_table", link["model"])
            if table_id not in entities_by_id:
                # fall back to any matching table
                table_id = None
                for eid, ent in entities_by_id.items():
                    if ent.entity_type.value == "database_table" and slugify(ent.name) == slugify(link["model"]):
                        table_id = eid
                        break
            sql_notes.append(
                SqlFieldNote(
                    database_entity_id=db_id,
                    table_entity_id=table_id,
                    field=link["model"],
                    purpose=link.get("purpose") or "",
                )
            )
            stats["sql_notes_from_links"] += 1
        for highlight in cap.get("field_highlights", []):
            db_name = highlight.get("database") or ""
            db_id = db_name_to_id.get(slugify(db_name)) if db_name else None
            table_id = None
            model = highlight.get("model") or ""
            if model:
                candidate = entity_id("database_table", model)
                if candidate in entities_by_id:
                    table_id = candidate
                else:
                    for eid, ent in entities_by_id.items():
                        if ent.entity_type.value == "database_table" and slugify(ent.name) == slugify(model):
                            table_id = eid
                            break
            sql_notes.append(
                SqlFieldNote(
                    database_entity_id=db_id,
                    table_entity_id=table_id,
                    field=highlight["field"],
                    purpose=highlight.get("meaning") or "",
                )
            )
            stats["sql_notes_from_highlights"] += 1

        when_to_use = cap.get("when_to_use")
        not_for = cap.get("not_for")
        incoming = {
            "role_paths": role_paths,
            "sql_field_notes": sql_notes,
            "description": cap.get("description") or cap.get("job") or "",
            "when_to_use": [when_to_use] if isinstance(when_to_use, str) and when_to_use else (when_to_use or []),
            "not_for": [not_for] if isinstance(not_for, str) and not_for else (not_for or []),
            "api_checks": cap.get("api_checks") or [],
            "source_refs": source_refs,
        }
        merged = merge_record(current, incoming)
        # Force-fill database_entity_id on existing notes that still lack it.
        filled_notes: list[SqlFieldNote] = []
        for note in merged.sql_field_notes:
            if note.database_entity_id is None:
                db_id = _database_id_for_table(note.table_entity_id, entities_by_id, db_name_to_id)
                if db_id:
                    note = note.model_copy(update={"database_entity_id": db_id})
                    stats["sql_notes_db_id_filled"] += 1
            filled_notes.append(note)
        if filled_notes != list(merged.sql_field_notes):
            merged = merged.model_copy(update={"sql_field_notes": filled_notes, "updated_at": _now()})
        elif merged is not current:
            merged = merged.model_copy(update={"updated_at": _now()})
        capabilities[cap_id] = merged
        stats["capabilities_enriched"] += 1

    # Fill remaining notes that still lack database_entity_id (stub caps etc.)
    for cap_id, cap in list(capabilities.items()):
        filled_notes = []
        changed = False
        for note in cap.sql_field_notes:
            if note.database_entity_id is None:
                db_id = _database_id_for_table(note.table_entity_id, entities_by_id, db_name_to_id)
                if db_id:
                    note = note.model_copy(update={"database_entity_id": db_id})
                    changed = True
                    stats["sql_notes_db_id_filled"] += 1
            filled_notes.append(note)
        if changed:
            capabilities[cap_id] = cap.model_copy(
                update={"sql_field_notes": filled_notes, "updated_at": _now()}
            )

    return capabilities, new_claims, dict(stats)


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _resolve_capability_ids_for_runbook(
    evidence: EvidenceUnit,
    payload: dict[str, Any],
    capabilities: dict[str, Capability],
    evidence_to_capabilities: dict[str, list[str]],
) -> list[str]:
    """Ordered unique capability ids for a runbook.

    Prefer capability_tags (catalog order = primary first). Fall back to
    Relationship(USES) edges when tags are missing. Never invent.
    """
    ordered: list[str] = []
    seen: set[str] = set()
    for tag in payload.get("capability_tags") or []:
        cap_id = _catalog_slug_to_capability_id(str(tag), capabilities)
        if cap_id and cap_id not in seen:
            ordered.append(cap_id)
            seen.add(cap_id)
    if ordered:
        return ordered
    for cap_id in evidence_to_capabilities.get(evidence.id, []):
        if cap_id in capabilities and cap_id not in seen:
            ordered.append(cap_id)
            seen.add(cap_id)
    return ordered


def _promote_runbook_to_procedures(
    evidence: EvidenceUnit,
    source_id: str,
    capabilities: dict[str, Capability],
    entities_by_id: dict[str, Entity],
    evidence_to_capabilities: dict[str, list[str]],
    table_index: dict[str, str],
    db_name_to_id: dict[str, str],
) -> tuple[list[Procedure], list[Claim], dict[str, list[SqlFieldNote]], str | None]:
    payload = evidence.content.structured_payload or {}
    steps_raw = payload.get("steps") or []
    if not steps_raw:
        return [], [], {}, "no_steps"

    cap_ids = _resolve_capability_ids_for_runbook(
        evidence, payload, capabilities, evidence_to_capabilities
    )
    if not cap_ids:
        return [], [], {}, "no_capability"

    procedures: list[Procedure] = []
    all_claims: list[Claim] = []
    notes_by_cap: dict[str, list[SqlFieldNote]] = {}

    for cap_id in cap_ids:
        proc, claims, extra_notes, skip = _promote_runbook_for_capability(
            evidence,
            source_id,
            cap_id,
            capabilities,
            entities_by_id,
            table_index,
            db_name_to_id,
        )
        if skip or proc is None:
            continue
        procedures.append(proc)
        all_claims.extend(claims)
        if extra_notes:
            notes_by_cap.setdefault(cap_id, []).extend(extra_notes)

    if not procedures:
        return [], [], {}, "empty_steps_after_parse"
    return procedures, all_claims, notes_by_cap, None


def _promote_runbook_for_capability(
    evidence: EvidenceUnit,
    source_id: str,
    cap_id: str,
    capabilities: dict[str, Capability],
    entities_by_id: dict[str, Entity],
    table_index: dict[str, str],
    db_name_to_id: dict[str, str],
) -> tuple[Procedure | None, list[Claim], list[SqlFieldNote], str | None]:
    payload = evidence.content.structured_payload or {}
    steps_raw = payload.get("steps") or []
    capability = capabilities[cap_id]
    proc_token = payload.get("procedure_id") or evidence.id.split(":")[-1]
    proc = Procedure(
        id=procedure_id(cap_id.split(":", 1)[-1], f"{source_id}_{slugify(str(proc_token))[:80]}"),
        capability_id=cap_id,
        procedure_type=capability.capability_kind,
        title=payload.get("title") or capability.name,
        summary=payload.get("summary") or "",
        when_to_use=_as_str_list(payload.get("when_to_use")),
        not_for=_as_str_list(payload.get("not_for")),
        allowed_role_entity_ids=[],
        steps=[],
        validation_status="needs_sme_review",
        source_refs=[evidence.id],
        created_at=_now(),
        updated_at=_now(),
    )

    role_ids: list[str] = []
    for role_name in (
        payload.get("role_required"),
        payload.get("responsible_role"),
        *(payload.get("supporting_roles") or []),
        *(payload.get("audience_roles") or []),
    ):
        rid = _resolve_role(str(role_name), entities_by_id) if role_name else None
        if rid and rid not in role_ids:
            role_ids.append(rid)
    proc = proc.model_copy(update={"allowed_role_entity_ids": role_ids})

    claims: list[Claim] = []
    extra_sql_notes: list[SqlFieldNote] = []
    built_steps: list[ProcedureStep] = []

    for idx, raw in enumerate(steps_raw, start=1):
        if not isinstance(raw, dict):
            continue
        resp = _resolve_role(str(raw.get("responsible_role") or ""), entities_by_id)
        supp = _resolve_role(str(raw.get("supporting_role") or ""), entities_by_id)
        actions: list[ProcedureAction] = []
        for action in raw.get("actions") or []:
            if not isinstance(action, dict):
                continue
            label = (action.get("label") or action.get("action_type") or "action").strip()
            exact = (action.get("exact_action") or "").strip()
            if not exact:
                continue
            action_role = _resolve_role(
                str(action.get("role_required") or raw.get("responsible_role") or ""),
                entities_by_id,
            )
            actions.append(
                ProcedureAction(
                    label=label[:200],
                    exact_action=exact,
                    role_entity_id=action_role,
                )
            )
            select_match = SELECT_RE.search(exact)
            if select_match:
                query_text = re.sub(r"\s+", " ", select_match.group(1)).strip()
                subject_id = _wcs_sql_entity_id(entities_by_id)
                table_match = FROM_TABLE_RE.search(query_text)
                table_eid = None
                if table_match:
                    table_name = table_match.group(1)
                    table_eid = table_index.get(slugify(table_name)) or table_index.get(table_name.lower())
                if subject_id is None and table_eid is not None:
                    subject_id = table_eid
                if subject_id is not None:
                    claims.append(
                        Claim(
                            id=claim_id(
                                slugify(cap_id),
                                f"approved_query_step_{idx}_{slugify(label)[:40]}",
                            ),
                            subject_entity_id=subject_id,
                            predicate="approved_ssms_query",
                            object=LiteralValueObject(value=query_text[:2000]),
                            polarity=Polarity.AFFIRMED,
                            condition=proc.id,
                            note=f"Exact query from procedure step {idx} ({label}).",
                            source_refs=[evidence.id],
                            created_at=_now(),
                            updated_at=_now(),
                        )
                    )
                if table_eid:
                    table_ent = entities_by_id[table_eid]
                    db_name = getattr(table_ent.payload, "database_name", None)
                    db_id = db_name_to_id.get(slugify(db_name)) if db_name else None
                    extra_sql_notes.append(
                        SqlFieldNote(
                            database_entity_id=db_id,
                            table_entity_id=table_eid,
                            field="*",
                            purpose=f"Queried by approved procedure step: {label}",
                        )
                    )

        stop_if = raw.get("stop_or_escalate_if") or []
        if isinstance(stop_if, str):
            stop_if = [stop_if]

        built_steps.append(
            ProcedureStep(
                step_number=idx,
                title=(raw.get("title") or f"Step {idx}")[:300],
                instruction=(raw.get("instruction") or raw.get("title") or "")[:4000],
                responsible_role_entity_id=resp,
                supporting_role_entity_id=supp,
                purpose=str(raw.get("purpose") or ""),
                expected_result=str(raw.get("expected_result") or ""),
                healthy_condition=str(raw.get("healthy_condition") or ""),
                failure_condition=str(raw.get("failure_condition") or ""),
                stop_or_escalate_if=[str(s) for s in stop_if if s],
                actions=actions,
                source_refs=[evidence.id],
            )
        )

    if not built_steps:
        return None, [], [], "empty_steps_after_parse"

    for i, step in enumerate(built_steps, start=1):
        if step.step_number != i:
            built_steps[i - 1] = step.model_copy(update={"step_number": i})

    proc = proc.model_copy(update={"steps": built_steps})
    return proc, claims, extra_sql_notes, None


def promote_operational_sources(
    capabilities: dict[str, Capability],
    entities_by_id: dict[str, Entity],
    ontology_claims: list[Claim],
) -> tuple[dict[str, list[Procedure]], dict[str, list[Relationship]], dict[str, list[Claim]], dict[str, int]]:
    stats = defaultdict(int)
    procedures_by_source: dict[str, list[Procedure]] = {}
    relationships_by_source: dict[str, list[Relationship]] = {}
    claims_by_source: dict[str, list[Claim]] = {}
    table_index = _table_name_index(list(entities_by_id.values()))
    db_name_to_id = _build_db_name_index(list(entities_by_id.values()))

    for source_dir in sorted(OPERATIONAL_DIR.iterdir()):
        if not source_dir.is_dir():
            continue
        source_id = source_dir.name
        evidence_units = _load_records(source_dir / "evidence_units.json", EvidenceUnit)
        relationships = _load_records(source_dir / "relationships.json", Relationship)

        evidence_to_capabilities: dict[str, list[str]] = defaultdict(list)
        for rel in relationships:
            if rel.relationship_type == RelationshipType.USES and rel.to_id.startswith("capability:"):
                if rel.to_id not in evidence_to_capabilities[rel.from_id]:
                    evidence_to_capabilities[rel.from_id].append(rel.to_id)

        procedures: list[Procedure] = []
        new_rels: list[Relationship] = []
        new_claims: list[Claim] = []

        for unit in evidence_units:
            payload = unit.content.structured_payload or {}
            if not payload.get("steps"):
                continue
            if "runbook" not in unit.id and not payload.get("procedure_id"):
                continue
            procs, claims, notes_by_cap, skip = _promote_runbook_to_procedures(
                unit,
                source_id,
                capabilities,
                entities_by_id,
                evidence_to_capabilities,
                table_index,
                db_name_to_id,
            )
            if skip:
                stats[f"skip_{skip}"] += 1
                continue
            for proc in procs:
                procedures.append(proc)
                stats["procedures_promoted"] += 1
                if any(
                    SELECT_RE.search(a.exact_action)
                    for step in proc.steps
                    for a in step.actions
                ):
                    stats["procedures_with_sql"] += 1
                new_rels.append(
                    Relationship(
                        id=relationship_id(proc.id, "uses", proc.capability_id),
                        from_id=proc.id,
                        relationship_type=RelationshipType.USES,
                        to_id=proc.capability_id,
                        note="Procedure carries out this capability (promoted from finalized runbook).",
                        source_refs=[unit.id],
                        created_at=_now(),
                        updated_at=_now(),
                    )
                )
            new_claims.extend(claims)
            for cap_id, extra_notes in notes_by_cap.items():
                cap = capabilities[cap_id]
                merged_notes = merge_list_field(cap.sql_field_notes, extra_notes)
                if merged_notes != cap.sql_field_notes:
                    capabilities[cap_id] = cap.model_copy(
                        update={"sql_field_notes": merged_notes, "updated_at": _now()}
                    )
                    stats["capability_sql_notes_from_procedures"] += len(extra_notes)

        procedures_by_source[source_id] = procedures
        relationships_by_source[source_id] = new_rels
        claims_by_source[source_id] = new_claims
        stats[f"source_{source_id}_procedures"] = len(procedures)

    return procedures_by_source, relationships_by_source, claims_by_source, dict(stats)


def run(*, write: bool) -> int:
    entities = _load_records(ONTOLOGY_DIR / "entities.json", Entity)
    entities_by_id = {e.id: e for e in entities}
    capabilities_list = _load_records(ONTOLOGY_DIR / "capabilities.json", Capability)
    capabilities = {c.id: c for c in capabilities_list}
    ontology_claims = _load_records(ONTOLOGY_DIR / "claims.json", Claim)
    ontology_relationships = _load_records(ONTOLOGY_DIR / "relationships.json", Relationship)
    ontology_evidence = _load_records(ONTOLOGY_DIR / "evidence_units.json", EvidenceUnit)

    db_name_to_id = _build_db_name_index(entities)
    capabilities, role_claims, cap_stats = enrich_capabilities_from_catalog(
        capabilities, entities_by_id, db_name_to_id
    )

    procedures_by_source, new_rels_by_source, new_claims_by_source, proc_stats = promote_operational_sources(
        capabilities, entities_by_id, ontology_claims
    )

    # Merge ontology role-path claims (dedupe by id)
    claim_by_id = {c.id: c for c in ontology_claims}
    for claim in role_claims:
        claim_by_id[claim.id] = claim

    all_procedures: list[Procedure] = []
    for procs in procedures_by_source.values():
        all_procedures.extend(procs)

    # Collect operational claims/rels for validation
    op_claims: list[Claim] = []
    op_rels: list[Relationship] = []
    op_evidence: list[EvidenceUnit] = []
    for source_dir in sorted(OPERATIONAL_DIR.iterdir()):
        if not source_dir.is_dir():
            continue
        op_evidence.extend(_load_records(source_dir / "evidence_units.json", EvidenceUnit))
        op_claims.extend(_load_records(source_dir / "claims.json", Claim))
        op_rels.extend(_load_records(source_dir / "relationships.json", Relationship))
        for claim in new_claims_by_source.get(source_dir.name, []):
            op_claims.append(claim)
        for rel in new_rels_by_source.get(source_dir.name, []):
            op_rels.append(rel)

    # Ensure claim subjects for approved queries resolve — drop claims whose
    # subject is missing (should not happen for wcs_sql).
    valid_query_claims: list[Claim] = []
    known_entity_ids = set(entities_by_id)
    for source_id, claims in new_claims_by_source.items():
        kept = []
        for claim in claims:
            if claim.subject_entity_id in known_entity_ids:
                kept.append(claim)
                valid_query_claims.append(claim)
        new_claims_by_source[source_id] = kept

    result = validate_batch(
        evidence_units=ontology_evidence + op_evidence,
        entities=entities,
        claims=list(claim_by_id.values()) + valid_query_claims,
        relationships=ontology_relationships + op_rels,
        capabilities=list(capabilities.values()),
        procedures=all_procedures,
    )

    print("=== enrich_brain_knowledge ===")
    print("capability enrichment:", cap_stats)
    print("procedure promotion:", proc_stats)
    print(f"procedures total: {len(all_procedures)}")
    print(f"role-path claims: {len(role_claims)}")
    print(f"query claims: {len(valid_query_claims)}")
    caps_with_roles = sum(1 for c in capabilities.values() if c.role_paths)
    caps_with_db = sum(
        1
        for c in capabilities.values()
        if any(n.database_entity_id for n in c.sql_field_notes)
    )
    notes_with_db = sum(
        1 for c in capabilities.values() for n in c.sql_field_notes if n.database_entity_id
    )
    notes_total = sum(len(c.sql_field_notes) for c in capabilities.values())
    print(f"capabilities with role_paths: {caps_with_roles}/{len(capabilities)}")
    print(f"capabilities with db-linked sql notes: {caps_with_db}")
    print(f"sql_field_notes with database_entity_id: {notes_with_db}/{notes_total}")
    print(f"validate_batch errors: {len(result.errors)}")
    for err in result.errors[:20]:
        print("  -", err)
    if result.errors:
        print("Refusing to write while validation fails.")
        return 1

    if not write:
        print("Dry run only. Re-run with --write to persist.")
        return 0

    dump_records(list(capabilities.values()), ONTOLOGY_DIR / "capabilities.json")
    dump_records(list(claim_by_id.values()), ONTOLOGY_DIR / "claims.json")

    for source_id, procedures in procedures_by_source.items():
        source_dir = OPERATIONAL_DIR / source_id
        dump_records(procedures, source_dir / "procedures.json")

        existing_claims = _load_records(source_dir / "claims.json", Claim)
        # Drop previous enrichment query claims so re-runs stay idempotent.
        claim_map = {
            c.id: c
            for c in existing_claims
            if c.predicate not in {"approved_ssms_query"}
        }
        for claim in new_claims_by_source.get(source_id, []):
            claim_map[claim.id] = claim
        dump_records(list(claim_map.values()), source_dir / "claims.json")

        existing_rels = _load_records(source_dir / "relationships.json", Relationship)
        # Replace prior procedure→capability USES edges from this enrichment.
        rel_map = {
            r.id: r
            for r in existing_rels
            if not (r.from_id.startswith("procedure:") and r.relationship_type == RelationshipType.USES)
        }
        for rel in new_rels_by_source.get(source_id, []):
            rel_map[rel.id] = rel
        dump_records(list(rel_map.values()), source_dir / "relationships.json")

    print("Wrote enriched capabilities, claims, procedures, and relationships.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Persist enrichment to brain/data/local/")
    args = parser.parse_args()
    raise SystemExit(run(write=args.write))


if __name__ == "__main__":
    main()
