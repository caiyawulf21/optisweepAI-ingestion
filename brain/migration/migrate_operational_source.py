"""Migrate one operationalknowledgeingestion source directory into Brain records.

Pass 1 of the Brain migration. Entity resolution runs against a shared
EntityRegistry so this can be seeded from the Pass 0 ontology-catalog
migration (brain/migration/migrate_ontology_catalogs.py) and run once per
source, accumulating one shared graph rather than five disconnected ones.

Nothing is dropped: every stage-4 context record becomes an Entity (or a
Claim referencing one), every stage-1 page/section becomes verbatim
EvidenceUnit, every stage-8 link becomes a Relationship, and every stage-5/6
record whose structure the current Part 1 schemas cannot model directly
(steps, capability_tags text, prerequisites, etc.) is preserved whole as an
EvidenceUnit.content.structured_payload so Part 2's procedure/playbook
schema has a lossless input later.

Run: python -m brain.migration.migrate_operational_source --source manual_optisweep_om_v3
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from brain.id_generation import capability_id, claim_id, evidence_id, relationship_id, slugify
from brain.migration.common import REPO_ROOT, content_hash, dump_records, load_json, load_json_dir
from brain.migration.entity_registry import EntityRegistry
from brain.migration.entity_shape import is_claim_shaped, strip_source_reference_leak
from brain.schemas.capability import Capability, CapabilityKind
from brain.schemas.claim import Claim, EntityRefObject, LiteralValueObject, Polarity
from brain.schemas.entity import Entity, EntityType
from brain.schemas.evidence_unit import EvidenceContent, EvidenceKind, EvidenceUnit
from brain.schemas.relationship import Relationship, RelationshipType
from brain.validators import validate_batch

OPERATIONAL_ROOT = REPO_ROOT / "operationalknowledgeingestion" / "data" / "output"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "brain" / "data" / "local" / "operational_sources"

# operational_context.context_type -> Brain EntityType. All 12 observed
# values are mapped; there is no fallback "unknown" bucket, so a new
# context_type in future source data will raise (KeyError) rather than
# silently miscategorize.
CONTEXT_TYPE_TO_ENTITY_TYPE: dict[str, EntityType] = {
    "system_overview": EntityType.SYSTEM,
    "hmi_screen_reference": EntityType.UI_SCREEN,
    "component_reference": EntityType.COMPONENT,
    "maintenance_reference": EntityType.COMPONENT,
    "operation_reference": EntityType.COMPONENT,
    "status_reference": EntityType.STATE,
    "alarm_reference": EntityType.ALARM,
    "hmi_metric_reference": EntityType.METRIC,
    "troubleshooting_reference": EntityType.SYMPTOM,
    "role_or_access_reference": EntityType.ROLE,
    "safety_reference": EntityType.COMPONENT,
    "glossary": EntityType.COMPONENT,
}

# stage_8 relationship_links.json link_type -> Brain RelationshipType.
LINK_TYPE_TO_RELATIONSHIP_TYPE: dict[str, RelationshipType] = {
    "artifact_context": RelationshipType.SUPPORTS,
    "context_runbook_shared_artifact": RelationshipType.SUPPORTS,
    "artifact_candidate": RelationshipType.SUPPORTS,
    "artifact_runbook": RelationshipType.SUPPORTS,
    "context_candidate": RelationshipType.SUPPORTS,
    "context_runbook": RelationshipType.SUPPORTS,
}

RECORD_TYPE_PREFIX = {
    "source_artifact": "artifact",
    "operational_context": "context",
    "runbook_candidate": "candidate",
    "finalized_runbook": "runbook",
}

_NUMBERED_ITEM_RE = re.compile(r"^(?P<label>.+?)\s*\(item\s*\d+\)\s*$", re.IGNORECASE)


def _split_item_label(point: str) -> tuple[str, bool]:
    """Return (label, is_numbered_component) for a what_to_look_at entry.

    A numbered diagram callout like "Tipper (Item 1)" unambiguously names a
    real physical component; strip the "(Item N)" suffix and promote it to a
    Component entity. Anything else ("Foot brake position
    (engaged/disengaged)") is an observation, not a new named thing, and is
    left for the caller to record as a Claim instead.
    """
    match = _NUMBERED_ITEM_RE.match(point.strip())
    if match:
        return match.group("label").strip(), True
    return point.strip(), False


class OperationalSourceMigration:
    def __init__(self, source_id: str, registry: EntityRegistry, capabilities: dict[str, Capability]) -> None:
        self.source_id = source_id
        self.registry = registry
        self.evidence_units: dict[str, EvidenceUnit] = {}
        self.claims: dict[str, Claim] = {}
        self.relationships: dict[str, Relationship] = {}
        # Shared with the caller (seeded from Pass 0) so a capability_tag
        # already defined by the ontology catalogs is reused, and one that
        # is genuinely new to this source is created rather than referenced
        # as a dangling relationship endpoint.
        self.capabilities = capabilities
        # non-Brain record id (e.g. "ctx_manual_..." or "artifact_fig_3_1...")
        # -> Brain typed id, so stage_8 links (which reference these raw ids)
        # can be resolved to real Relationship endpoints.
        self.raw_id_to_brain_id: dict[str, str] = {}

    def _get_or_create_capability(self, tag: str, *, source_refs: list[str]) -> Capability:
        cap_id = capability_id(tag)
        existing = self.capabilities.get(cap_id)
        if existing is not None:
            merged = list(dict.fromkeys([*existing.source_refs, *source_refs]))
            if merged != existing.source_refs:
                existing = existing.model_copy(update={"source_refs": merged})
                self.capabilities[cap_id] = existing
            return existing
        capability = Capability(
            id=cap_id,
            name=tag.replace("_", " ").title(),
            capability_kind=CapabilityKind.DIAGNOSTIC,
            source_refs=source_refs,
        )
        self.capabilities[cap_id] = capability
        return capability

    # -- helpers ----------------------------------------------------------

    def _add_evidence(
        self,
        *,
        id_parts: list[str],
        evidence_kind: EvidenceKind,
        text: str | None,
        is_verbatim: bool,
        page: int | None = None,
        section: str | None = None,
        video_start_seconds: float | None = None,
        video_end_seconds: float | None = None,
        structured_payload: dict[str, Any] | None = None,
    ) -> EvidenceUnit | None:
        text = text.strip() if text else None
        if not text and not structured_payload:
            # Nothing to cite: no verbatim/derived text and no raw structure
            # to fall back on. Caller should treat a None return as "skipped,
            # no content" rather than force a placeholder string into what the
            # schema requires to be real evidentiary text (Part 1 §4).
            return None
        unit_id = evidence_id(self.source_id, ":".join(slugify(p) for p in id_parts))
        unit = EvidenceUnit(
            id=unit_id,
            evidence_kind=evidence_kind,
            source_type="manual" if "manual" in self.source_id else "training_video",
            source_id=f"source:{self.source_id}",
            content=EvidenceContent(
                text=text,
                is_verbatim=is_verbatim,
                content_hash=content_hash(unit_id, text or json.dumps(structured_payload, default=str)),
                structured_payload=structured_payload,
            ),
            locator={
                "page": page,
                "section": section,
                "video_start_seconds": video_start_seconds,
                "video_end_seconds": video_end_seconds,
            },
            source_refs=[f"source:{self.source_id}"],
        )
        self.evidence_units[unit.id] = unit
        return unit

    def _add_relationship(
        self, from_id: str, rel_type: RelationshipType, to_id: str, *, source_refs: list[str], note: str = ""
    ) -> None:
        rel_id = relationship_id(from_id, rel_type.value, to_id)
        if rel_id in self.relationships:
            existing = self.relationships[rel_id]
            merged = list(dict.fromkeys([*existing.source_refs, *source_refs]))
            if merged != existing.source_refs:
                self.relationships[rel_id] = existing.model_copy(update={"source_refs": merged})
            return
        self.relationships[rel_id] = Relationship(
            id=rel_id, from_id=from_id, relationship_type=rel_type, to_id=to_id, note=note, source_refs=source_refs
        )

    # -- stage 1: verbatim source text -------------------------------------

    def migrate_stage1(self, source_dir: Path) -> None:
        slide_segments_path = source_dir / "stage_1_source_bundle" / "training_video_slide_segments.json"
        if slide_segments_path.exists():
            self._migrate_training_video_segments(slide_segments_path)
            return

        bundle_path = source_dir / "stage_1_source_bundle" / "source_bundle.json"
        if not bundle_path.exists():
            print(f"  (no stage_1 source_bundle.json for {self.source_id})")
            return
        bundle = load_json(bundle_path)

        empty_sections = 0
        for section in bundle.get("sections", []):
            unit = self._add_evidence(
                id_parts=["section", section["section_id"]],
                evidence_kind=EvidenceKind.DOCUMENT_SECTION,
                text=section.get("text_preview", ""),
                is_verbatim=True,
                page=section.get("page_start"),
                section=section["section_id"],
            )
            if unit is None:
                empty_sections += 1
        empty_pages = 0
        for page in bundle.get("pages", []):
            unit = self._add_evidence(
                id_parts=["page", str(page["page_number"])],
                evidence_kind=EvidenceKind.DOCUMENT_SECTION,
                text=page.get("text", ""),
                is_verbatim=True,
                page=page.get("page_number"),
                section=page.get("section_id"),
            )
            if unit is None:
                empty_pages += 1
        if empty_sections or empty_pages:
            print(f"  (skipped {empty_sections} empty section(s), {empty_pages} empty page(s) with no body text)")

    def _migrate_training_video_segments(self, path: Path) -> None:
        # Training video sources produce training_video_slide_segments.json at
        # Stage 1 rather than a page/section source_bundle.json; a synthesized
        # pages-shaped source_bundle.json also exists under stage_2 purely so
        # Stage 4/5 tooling can read it, but it is a lossy restringing of these
        # same segments (transcript_text/ocr_confidence/video timestamps
        # collapse into one text blob) — migrating that too would duplicate
        # every piece of evidence, so this is the sole Stage 1 evidence source
        # for a training-video source.
        segments = load_json(path)
        empty = 0
        for seg in segments:
            transcript = (seg.get("transcript_text") or "").strip()
            ocr = (seg.get("ocr_text") or "").strip()
            text = transcript or ocr
            unit = self._add_evidence(
                id_parts=["segment", seg["segment_id"]],
                evidence_kind=EvidenceKind.TRAINING_VIDEO_SEGMENT,
                text=text,
                is_verbatim=True,
                video_start_seconds=seg.get("start_time_seconds"),
                video_end_seconds=seg.get("end_time_seconds"),
                structured_payload={
                    "segment_id": seg["segment_id"],
                    "artifact_ids": seg.get("artifact_ids", []),
                    "transcript_cues": seg.get("transcript_cues", []),
                    "ocr_confidence": seg.get("ocr_confidence"),
                    "has_transcript": bool(transcript),
                },
            )
            if unit is None:
                empty += 1
            else:
                self.raw_id_to_brain_id[seg["segment_id"]] = unit.id
        if empty:
            print(f"  (skipped {empty} training video segment(s) with no transcript or OCR text)")

    # -- stage 2/3: artifacts (raw + vision enrichment) ----------------------

    def migrate_artifacts(self, source_dir: Path) -> None:
        enriched_path = source_dir / "stage_3_artifact_enrichment" / "source_artifacts_enriched.json"
        raw_path = source_dir / "stage_2_source_artifacts" / "source_artifacts.json"
        path = enriched_path if enriched_path.exists() else raw_path
        if not path.exists():
            print(f"  (no source_artifacts for {self.source_id})")
            return
        artifacts = load_json(path)

        promoted_components = 0
        promoted_claims = 0

        for artifact in artifacts:
            raw_id = artifact["artifact_id"]
            # structured_payload guarantees a non-None return even when
            # caption/nearby_text are both empty (storage_path always exists).
            verbatim_unit = self._add_evidence(
                id_parts=["artifact", raw_id, "verbatim"],
                evidence_kind=EvidenceKind.IMAGE_OR_OCR_REGION,
                text=f"{artifact.get('caption_text', '')} {artifact.get('nearby_text', '')}".strip(),
                is_verbatim=True,
                page=artifact.get("page_number"),
                section=artifact.get("section_id"),
                structured_payload={"artifact_id": raw_id, "storage_path": artifact.get("storage_path")},
            )
            assert verbatim_unit is not None
            self.raw_id_to_brain_id[raw_id] = verbatim_unit.id

            enrichment_fields = {
                k: artifact.get(k)
                for k in ("detailed_description", "short_description", "tags", "what_to_look_at", "enrichment_notes")
                if artifact.get(k)
            }
            if not enrichment_fields:
                continue

            enrichment_unit = self._add_evidence(
                id_parts=["artifact", raw_id, "enrichment"],
                evidence_kind=EvidenceKind.IMAGE_OR_OCR_REGION,
                text=enrichment_fields.get("detailed_description") or artifact.get("summary", ""),
                is_verbatim=False,
                page=artifact.get("page_number"),
                section=artifact.get("section_id"),
                structured_payload={"artifact_id": raw_id, **enrichment_fields},
            )
            assert enrichment_unit is not None

            # Promote vision content into the knowledge graph rather than
            # leaving it as inert evidence: a numbered callout ("Tipper (Item
            # 1)") names a real physical component, so it becomes a Component
            # entity DISPLAYED by this artifact. An unlabeled observation
            # ("Foot brake position (engaged/disengaged)") is a claim ABOUT
            # the artifact/component, not a new named thing, so it becomes a
            # Claim instead of a speculative entity.
            for point in artifact.get("what_to_look_at", []):
                label, is_numbered_component = _split_item_label(point)
                if is_numbered_component:
                    comp_entity = self.registry.get_or_create(
                        EntityType.COMPONENT,
                        label,
                        source_refs=[enrichment_unit.id],
                    )
                    self._add_relationship(
                        verbatim_unit.id,
                        RelationshipType.DISPLAYS,
                        comp_entity.id,
                        source_refs=[enrichment_unit.id],
                        note=f"artifact {raw_id} displays {label}",
                    )
                    promoted_components += 1
                else:
                    c_id = claim_id(f"{raw_id}_{slugify(point)[:40]}", "observes")
                    self.claims[c_id] = Claim(
                        id=c_id,
                        subject_entity_id=self._artifact_subject_entity(artifact, enrichment_unit.id).id,
                        predicate="observed_in_artifact",
                        object=LiteralValueObject(kind="literal", value=point),
                        polarity=Polarity.AFFIRMED,
                        source_refs=[enrichment_unit.id],
                    )
                    promoted_claims += 1

            if artifact.get("detailed_description"):
                c_id = claim_id(raw_id, "detailed_description")
                self.claims[c_id] = Claim(
                    id=c_id,
                    subject_entity_id=self._artifact_subject_entity(artifact, enrichment_unit.id).id,
                    predicate="has_visual_description",
                    object=LiteralValueObject(kind="literal", value=artifact["detailed_description"]),
                    polarity=Polarity.AFFIRMED,
                    source_refs=[enrichment_unit.id],
                )
                promoted_claims += 1

            # Tag -> capability linking is deliberately NOT done here by
            # keyword overlap. A tag like "tipper" and a capability slug like
            # tipper_station_fault share a word but not necessarily meaning:
            # a photo of tipper hardware is not evidence the photo supports
            # fault diagnosis. Deciding that link requires understanding what
            # the artifact actually shows, which is semantic extraction work
            # for the future LLM-assisted reconciliation step (see
            # brain/migration/BRAIN_BUILD_PROCESS.md, "Deferred to LLM
            # extraction"), not a string-matching heuristic. `tags` remain
            # available verbatim in enrichment_unit.content.structured_payload
            # so that future step has the raw input to work from.

        if promoted_components or promoted_claims:
            print(
                f"  (promoted from vision enrichment: {promoted_components} component entities, "
                f"{promoted_claims} claims)"
            )

    def _artifact_subject_entity(self, artifact: dict, evidence_id_for_new_entity: str) -> Entity:
        # Claims need a subject_entity_id (Part 1 §7), but an artifact itself
        # is evidence, not an entity. Resolve to the component/screen entity
        # the artifact is filed under when known (its title), else fall back
        # to a component entity representing the artifact's own subject.
        #
        # A training-video artifact's "title" can be raw OCR'd slide footer
        # text ("Overview What is Optisweep? 3 FORTNA ALL RIGHTS RESERVED...")
        # rather than a real name — is_claim_shaped's sentence-length check
        # catches this reliably. Falling back to the artifact_id in that case
        # produces an uninformative but stable and honest label, rather than
        # promoting garbled OCR text into the entity registry as if it named
        # something real.
        title = artifact.get("title")
        name = title if title and not is_claim_shaped(title) else artifact["artifact_id"]
        return self.registry.get_or_create(
            EntityType.COMPONENT, name, source_refs=[evidence_id_for_new_entity]
        )

    # -- stage 4: operational context -> Entity + Claim ---------------------

    def migrate_operational_context(self, source_dir: Path) -> None:
        path = source_dir / "stage_4_operational_context" / "operational_context.json"
        if not path.exists():
            print(f"  (no operational_context.json for {self.source_id})")
            return
        records = load_json(path)

        # Two-pass: a record's title can read as a real name ("Operator
        # Station HMI") or as a claim/procedure ("Apply Power to Tipper
        # Station", "Dependence on dimension data rather than chute sensors").
        # is_claim_shaped() makes that call per-record — context_type is not
        # a reliable signal (an audit of the existing registry found the
        # mis-modeled entities spread across nearly every context_type, not
        # concentrated in one or two — see BRAIN_BUILD_PROCESS.md). Claim-shaped
        # records are processed in a SECOND pass so their applies_to values
        # can resolve against entities the first pass already created in this
        # same source (records are not grouped by context_type in the source
        # file, so processing order alone doesn't guarantee this without the
        # split).
        claim_shaped_records = []
        for rec in records:
            evidence_ids = self._context_record_evidence(rec)

            if is_claim_shaped(rec["title"]):
                claim_shaped_records.append((rec, evidence_ids))
                continue

            self._migrate_named_context_record(rec, evidence_ids)

        unresolved = 0
        for rec, evidence_ids in claim_shaped_records:
            if not self._migrate_claim_shaped_context_record(rec, evidence_ids):
                unresolved += 1
        if unresolved:
            print(
                f"  ({unresolved} claim-shaped context record(s) had no applies_to entry "
                f"resolving to a known entity; kept as evidence only, no claim created)"
            )

    def _context_record_evidence(self, rec: dict) -> list[str]:
        evidence_ids: list[str] = []
        for idx, ref in enumerate(rec.get("source_refs", [])):
            unit = self._add_evidence(
                id_parts=["context", rec["context_id"], "ref", str(idx)],
                evidence_kind=EvidenceKind.DOCUMENT_SECTION,
                text=ref.get("quote_or_summary", ""),
                is_verbatim=True,
                page=ref.get("page"),
                section=ref.get("section_id"),
            )
            if unit is not None:
                evidence_ids.append(unit.id)
        if not evidence_ids:
            # Fall back to the record itself (title/context_id) rather than
            # skipping the whole context record when every source_ref quote
            # was empty and summary is also empty (title always exists).
            unit = self._add_evidence(
                id_parts=["context", rec["context_id"], "summary"],
                evidence_kind=EvidenceKind.DOCUMENT_SECTION,
                text=rec.get("summary") or rec.get("title", ""),
                is_verbatim=False,
                structured_payload={"context_id": rec["context_id"]},
            )
            assert unit is not None
            evidence_ids = [unit.id]
        return evidence_ids

    def _migrate_named_context_record(self, rec: dict, evidence_ids: list[str]) -> None:
        context_type = rec["context_type"]
        entity_type = CONTEXT_TYPE_TO_ENTITY_TYPE[context_type]

        # `title` is the specific, per-record name (e.g. "OptiSweep O&M
        # Manual Document Structure"). `applies_to` is a broad scope tag
        # ("OptiSweep system") shared by dozens of unrelated records — it
        # must never be used as the entity name or every one of those
        # records collapses onto the same entity. It becomes an
        # APPLIES_TO relationship to the broader system/component entity
        # instead, which is what it actually means.
        entity_name = rec["title"]
        payload: dict[str, Any] = {}
        if entity_type is EntityType.UI_SCREEN:
            payload = {
                "surface": (rec.get("applies_to") or ["unknown"])[0],
                "navigation_hint": [],
                "visible_fields": [{"name": t, "meaning": t} for t in rec.get("key_terms", [])],
                "artifact_ids": [
                    self.raw_id_to_brain_id[a]
                    for a in rec.get("related_artifact_ids", [])
                    if a in self.raw_id_to_brain_id
                ],
            }
        elif entity_type is EntityType.SYSTEM:
            payload = {"operational_roles": [], "owned_domains": [], "health_surfaces": []}

        entity = self.registry.get_or_create(
            entity_type,
            entity_name,
            description=strip_source_reference_leak(rec.get("summary", "")),
            aliases=rec.get("key_terms", []),
            payload=payload,
            source_refs=evidence_ids,
        )
        self.raw_id_to_brain_id[rec["context_id"]] = entity.id

        for scope_name in rec.get("applies_to", []):
            if not scope_name or scope_name.strip().lower() == entity_name.strip().lower():
                continue
            if is_claim_shaped(scope_name):
                # An applies_to value can itself be claim-shaped ("Add Robot
                # function", not a real system) rather than a genuine scope
                # entity — the same category error _migrate_named_context_record
                # guards against for record titles applies here too, on a
                # different code path that was found missing this check
                # during the entity-vs-claim audit.
                continue
            scope_entity = self.registry.get_or_create(
                EntityType.SYSTEM, scope_name, source_refs=evidence_ids
            )
            if scope_entity.id == entity.id:
                # The raw-string check above only catches an exact title
                # match; scope_name can also resolve (via an alias/key_term
                # already on `entity`) to this SAME entity under a different
                # spelling — get_or_create following that alias back to
                # `entity` itself would otherwise produce a meaningless
                # self-referential APPLIES_TO edge (found during the
                # ambiguous-entity reclassification pass; see
                # BRAIN_BUILD_PROCESS.md).
                continue
            self._add_relationship(
                entity.id,
                RelationshipType.APPLIES_TO,
                scope_entity.id,
                source_refs=evidence_ids,
                note=f"{entity_name} applies to {scope_name}",
            )

        # The record's `details` text is an assertion beyond the bare
        # entity description; keep it as a Claim about the entity so it
        # is not silently dropped, with polarity affirmed (Stage 4 output
        # here is treated as source-backed, not speculative).
        if rec.get("details"):
            c_id = claim_id(rec["context_id"], "details")
            self.claims[c_id] = Claim(
                id=c_id,
                subject_entity_id=entity.id,
                predicate="has_detail",
                object=LiteralValueObject(kind="literal", value=strip_source_reference_leak(rec["details"])),
                polarity=Polarity.AFFIRMED,
                source_refs=evidence_ids,
            )

    def _migrate_claim_shaped_context_record(self, rec: dict, evidence_ids: list[str]) -> bool:
        # A claim-shaped title/record never becomes its own Entity. Resolve
        # applies_to against entities already known to the registry (Pass 0
        # catalog entities, plus this source's own named-context-record pass,
        # which already ran); attach the record's content as a Claim on the
        # first entity that resolves. If nothing resolves, the record's
        # content is still fully preserved in evidence_ids — it is simply not
        # promoted to a structured Claim, since a Claim requires a real
        # subject_entity_id (Part 1 §7) and fabricating one would recreate
        # the exact problem this function exists to avoid.
        #
        # Either way, raw_id_to_brain_id MUST be set for this context_id: a
        # stage_8 relationship_links.json entry may reference it, and leaving
        # the mapping unset would make that link silently unresolvable (this
        # was a real regression caught by the stage_8 unresolved-link count
        # rising after this function was first written — see
        # BRAIN_BUILD_PROCESS.md). When no claim subject resolves, the primary
        # EvidenceUnit is the closest real Brain record this context_id maps
        # to, so links point there instead of at nothing.
        subject_entity = None
        for candidate_name in rec.get("applies_to", []):
            for entity_type in EntityType:
                found = self.registry.resolve(entity_type, candidate_name)
                if found is not None:
                    subject_entity = found
                    break
            if subject_entity is not None:
                break

        if subject_entity is None:
            self.raw_id_to_brain_id[rec["context_id"]] = evidence_ids[0]
            return False

        claim_text = strip_source_reference_leak(rec.get("details") or rec.get("summary") or rec["title"])
        c_id = claim_id(rec["context_id"], "context_fact")
        self.claims[c_id] = Claim(
            id=c_id,
            subject_entity_id=subject_entity.id,
            predicate="has_related_fact",
            object=LiteralValueObject(kind="literal", value=claim_text),
            polarity=Polarity.AFFIRMED,
            source_refs=evidence_ids,
        )
        self.raw_id_to_brain_id[rec["context_id"]] = subject_entity.id
        return True

    # -- stage 5/6: candidates and finalized runbooks (staged whole) --------

    def migrate_runbook_records(self, source_dir: Path) -> None:
        # structured_payload=rec guarantees a non-None return in both loops
        # below even if summary/title are both empty.
        candidates_path = source_dir / "stage_5_runbook_candidates" / "runbook_candidates.json"
        if candidates_path.exists():
            for rec in load_json(candidates_path):
                unit = self._add_evidence(
                    id_parts=["candidate", rec["candidate_id"]],
                    evidence_kind=EvidenceKind.SME_NOTE,
                    text=rec.get("summary", rec.get("title", "")),
                    is_verbatim=False,
                    structured_payload=rec,
                )
                assert unit is not None
                self.raw_id_to_brain_id[rec["candidate_id"]] = unit.id

        finalized_dir = source_dir / "stage_6_finalized_runbooks" / "finalized_runbooks"
        for rec in load_json_dir(finalized_dir):
            unit = self._add_evidence(
                id_parts=["runbook", rec["procedure_id"]],
                evidence_kind=EvidenceKind.SME_NOTE,
                text=rec.get("summary", rec.get("title", "")),
                is_verbatim=False,
                structured_payload=rec,
            )
            assert unit is not None
            self.raw_id_to_brain_id[rec["procedure_id"]] = unit.id
            if rec.get("candidate_id"):
                self.raw_id_to_brain_id.setdefault(rec["candidate_id"], unit.id)

            for tag in rec.get("capability_tags", []) or []:
                cap = self._get_or_create_capability(tag, source_refs=[unit.id])
                self._add_relationship(
                    unit.id,
                    RelationshipType.USES,
                    cap.id,
                    source_refs=[unit.id],
                    note=f"finalized runbook {rec['procedure_id']} tagged with capability {tag}",
                )

    # -- stage 8: relationship links -----------------------------------------

    def migrate_relationship_links(self, source_dir: Path) -> None:
        path = source_dir / "stage_8_relationship_linking" / "relationship_links.json"
        if not path.exists():
            print(f"  (no relationship_links.json for {self.source_id})")
            return
        links = load_json(path)
        unresolved = 0
        for link in links:
            from_raw = link["source_record_id"]
            to_raw = link["target_record_id"]
            from_id = self.raw_id_to_brain_id.get(from_raw)
            to_id = self.raw_id_to_brain_id.get(to_raw)
            if not from_id or not to_id:
                unresolved += 1
                continue
            rel_type = LINK_TYPE_TO_RELATIONSHIP_TYPE.get(link["link_type"], RelationshipType.SUPPORTS)
            self._add_relationship(
                from_id,
                rel_type,
                to_id,
                source_refs=[from_id],
                note=f"{link['link_type']} via {link['link_method']}",
            )
        if unresolved:
            print(f"  ({unresolved}/{len(links)} stage_8 links could not resolve to a migrated record)")

    # -- entrypoint -----------------------------------------------------

    def run(self, source_dir: Path) -> None:
        self.migrate_stage1(source_dir)
        self.migrate_artifacts(source_dir)
        self.migrate_operational_context(source_dir)
        self.migrate_runbook_records(source_dir)
        self.migrate_relationship_links(source_dir)


def migrate_source(
    source_id: str, registry: EntityRegistry, output_root: Path, capabilities: dict[str, Capability]
) -> dict[str, int]:
    source_dir = OPERATIONAL_ROOT / source_id
    if not source_dir.is_dir():
        raise SystemExit(f"source directory not found: {source_dir}")

    migration = OperationalSourceMigration(source_id, registry, capabilities)
    migration.run(source_dir)

    result = validate_batch(
        evidence_units=migration.evidence_units.values(),
        entities=registry.all(),
        claims=migration.claims.values(),
        relationships=migration.relationships.values(),
        capabilities=capabilities.values(),
    )
    if not result.valid:
        print(f"VALIDATION FAILED for {source_id}: {len(result.errors)} error(s)")
        for error in result.errors[:50]:
            print(f"  - {error}")
        raise SystemExit(1)

    out_dir = output_root / source_id
    counts = {
        "evidence_units": dump_records(list(migration.evidence_units.values()), out_dir / "evidence_units.json"),
        "claims": dump_records(list(migration.claims.values()), out_dir / "claims.json"),
        "relationships": dump_records(list(migration.relationships.values()), out_dir / "relationships.json"),
    }
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Source directory name under operationalknowledgeingestion/data/output/")
    parser.add_argument(
        "--registry-in",
        type=Path,
        default=REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs" / "entities.json",
        help="Path to entities.json to seed the registry from (Pass 0 output).",
    )
    parser.add_argument(
        "--registry-out",
        type=Path,
        default=None,
        help="Where to write the updated entities.json (default: overwrite --registry-in).",
    )
    parser.add_argument(
        "--capabilities-in",
        type=Path,
        default=REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs" / "capabilities.json",
        help="Path to capabilities.json to seed from (Pass 0 output).",
    )
    parser.add_argument(
        "--capabilities-out",
        type=Path,
        default=None,
        help="Where to write the updated capabilities.json (default: overwrite --capabilities-in).",
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args()

    registry = EntityRegistry()
    if args.registry_in.exists():
        for raw in load_json(args.registry_in):
            entity = Entity.model_validate(raw)
            registry.entities[entity.id] = entity
            registry._index_aliases(entity)
        print(f"Seeded registry with {len(registry.entities)} entities from {args.registry_in}")

    capabilities: dict[str, Capability] = {}
    if args.capabilities_in.exists():
        for raw in load_json(args.capabilities_in):
            cap = Capability.model_validate(raw)
            capabilities[cap.id] = cap
        print(f"Seeded {len(capabilities)} capabilities from {args.capabilities_in}")

    counts = migrate_source(args.source, registry, args.output_root, capabilities)

    registry_out = args.registry_out or args.registry_in
    dump_records(registry.all(), registry_out)

    capabilities_out = args.capabilities_out or args.capabilities_in
    dump_records(list(capabilities.values()), capabilities_out)

    print(f"Operational source migration complete: {args.source}")
    for name, count in counts.items():
        print(f"  {name}: {count}")
    print(f"  entities (registry total): {len(registry.entities)}")
    print(f"  capabilities (total): {len(capabilities)}")


if __name__ == "__main__":
    main()
