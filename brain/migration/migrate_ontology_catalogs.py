"""Migrate docs/ontology/catalogs/ into Brain records.

This is Pass 0 of the Brain migration (see brain/migration/README.md): the
ontology catalogs are hand-curated, already ontology-shaped, and authoritative
for OptiSweep's systems, screens, databases, and capabilities. They are
migrated first, and every later pass resolves entity names against the
registry this script produces before creating anything new (Part 1 §9).

Run: python -m brain.migration.migrate_ontology_catalogs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from brain.id_generation import capability_id, claim_id, evidence_id, make_id, relationship_id, slugify
from brain.migration.entity_registry import EntityRegistry
from brain.migration.merge import merge_record
from brain.schemas.capability import (
    Capability,
    CapabilityKind,
    Observables,
    RolePathGuidance,
    SqlFieldNote,
    SupportContract,
)
from brain.schemas.claim import Claim, LiteralValueObject, Polarity
from brain.schemas.entity import Entity, EntityType
from brain.schemas.evidence_unit import EvidenceContent, EvidenceKind, EvidenceUnit
from brain.schemas.relationship import Relationship, RelationshipType
from brain.validators import validate_batch

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOGS_DIR = REPO_ROOT / "docs" / "ontology" / "catalogs"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs"

# Surface catalogs share surface_catalog_schema.json. capability_catalog,
# wcs_sql_catalog, and cross_links have their own shapes and are handled by
# dedicated functions below.
SURFACE_CATALOG_FILES = [
    "apidog_catalog.json",
    "aveva_hmi_catalog.json",
    "building_acb_hmi_catalog.json",
    "event_viewer_catalog.json",
    "hospital_hmi_catalog.json",
    "ignition_gateway_catalog.json",
    "physical_floor_catalog.json",
    "rms_ui_catalog.json",
    "site_interview_catalog.json",
    "stunnel_catalog.json",
    "tipper_hmi_catalog.json",
    "wcs_api_catalog.json",
]

CAPABILITY_KIND_BY_PREFIX = {
    "verify": CapabilityKind.VERIFICATION,
    "check": CapabilityKind.VERIFICATION,
    "query": CapabilityKind.DIAGNOSTIC,
    "restart": CapabilityKind.RECOVERY,
    "recover": CapabilityKind.RECOVERY,
    "clear": CapabilityKind.RECOVERY,
}


def _content_hash(*parts: str) -> str:
    import hashlib

    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"sha256:{digest}"


def _capability_kind_for(activity_id: str) -> CapabilityKind:
    lowered = activity_id.lower()
    for prefix, kind in CAPABILITY_KIND_BY_PREFIX.items():
        if prefix in lowered:
            return kind
    return CapabilityKind.DIAGNOSTIC


class CatalogMigration:
    def __init__(self) -> None:
        self.registry = EntityRegistry()
        self.evidence_units: dict[str, EvidenceUnit] = {}
        self.capabilities: dict[str, Capability] = {}
        self.claims: dict[str, Claim] = {}
        self.relationships: dict[str, Relationship] = {}
        # capability slug (e.g. "agv_active_errors") -> capability record id
        self._capability_index: dict[str, str] = {}
        # failure_pattern / symptom slug -> entity id
        self._symptom_index: dict[str, str] = {}

    # -- shared helpers --------------------------------------------------

    def _add_evidence(
        self,
        *,
        id_parts: list[str],
        text: str,
        source_id: str,
        evidence_kind: EvidenceKind = EvidenceKind.SME_NOTE,
        section: str | None = None,
    ) -> EvidenceUnit:
        unit_id = evidence_id(source_id, ":".join(slugify(p) for p in id_parts))
        if unit_id in self.evidence_units:
            return self.evidence_units[unit_id]
        unit = EvidenceUnit(
            id=unit_id,
            evidence_kind=evidence_kind,
            source_type="ontology_catalog",
            source_id=source_id,
            content=EvidenceContent(
                text=text,
                is_verbatim=False,
                content_hash=_content_hash(unit_id, text),
            ),
            locator={"section": section} if section else {},
            source_refs=[source_id],
        )
        self.evidence_units[unit.id] = unit
        return unit

    def _get_or_create_capability(
        self,
        capability_slug: str,
        *,
        label: str | None = None,
        description: str = "",
        when_to_use: list[str] | None = None,
        not_for: list[str] | None = None,
        api_checks: list[str] | None = None,
        observables: Observables | None = None,
        support_contract: SupportContract | None = None,
        source_refs: list[str] | None = None,
    ) -> Capability:
        incoming_fields = {
            "name": label,
            "description": description,
            "when_to_use": when_to_use or [],
            "not_for": not_for or [],
            "api_checks": api_checks or [],
            "observables": observables,
            "support_contract": support_contract,
            "source_refs": source_refs or [],
        }
        if capability_slug in self._capability_index:
            existing = self.capabilities[self._capability_index[capability_slug]]
            merged = merge_record(existing, incoming_fields)
            if merged is not existing:
                self.capabilities[merged.id] = merged
            return merged

        cap_id = capability_id(capability_slug)
        capability = Capability(
            id=cap_id,
            name=label or capability_slug.replace("_", " ").title(),
            description=description,
            capability_kind=_capability_kind_for(capability_slug),
            when_to_use=when_to_use or [],
            not_for=not_for or [],
            api_checks=api_checks or [],
            observables=observables or Observables(),
            support_contract=support_contract,
            source_refs=source_refs or [],
        )
        self.capabilities[cap_id] = capability
        self._capability_index[capability_slug] = cap_id
        return capability

    def _get_or_create_symptom(self, failure_pattern_slug: str, *, source_refs: list[str]) -> Entity:
        if failure_pattern_slug in self._symptom_index:
            entity_id_ = self._symptom_index[failure_pattern_slug]
            existing = self.registry.entities[entity_id_]
            merged = merge_record(existing, {"source_refs": source_refs})
            if merged is not existing:
                self.registry.entities[merged.id] = merged
            return merged
        entity = self.registry.get_or_create(
            EntityType.SYMPTOM,
            failure_pattern_slug.replace("_", " "),
            aliases=[failure_pattern_slug],
            source_refs=source_refs,
        )
        self._symptom_index[failure_pattern_slug] = entity.id
        return entity

    def _add_relationship(
        self,
        from_id: str,
        relationship_type: RelationshipType,
        to_id: str,
        *,
        source_refs: list[str],
        note: str = "",
    ) -> Relationship:
        rel_id = relationship_id(from_id, relationship_type.value, to_id)
        if rel_id in self.relationships:
            existing = self.relationships[rel_id]
            merged = list(dict.fromkeys([*existing.source_refs, *source_refs]))
            if merged != existing.source_refs:
                existing = existing.model_copy(update={"source_refs": merged})
                self.relationships[rel_id] = existing
            return existing
        rel = Relationship(
            id=rel_id,
            from_id=from_id,
            relationship_type=relationship_type,
            to_id=to_id,
            note=note,
            source_refs=source_refs,
        )
        self.relationships[rel_id] = rel
        return rel

    # -- surface catalogs --------------------------------------------------

    def migrate_surface_catalog(self, data: dict[str, Any]) -> None:
        catalog_id: str = data["catalog_id"]
        access_surface: str = data["access_surface"]
        title: str = data.get("title", access_surface)
        aliases: list[str] = data.get("aliases", [])
        purpose: str = data.get("purpose", "")

        source_id = f"catalog:{catalog_id}"

        # Evidence: each catalog's evidence[] array is bounded snippet+source.
        evidence_ids: list[str] = []
        for idx, item in enumerate(data.get("evidence", [])):
            unit = self._add_evidence(
                id_parts=[catalog_id, "evidence", str(idx)],
                text=item.get("snippet", ""),
                source_id=item.get("source", source_id),
            )
            evidence_ids.append(unit.id)
        if not evidence_ids:
            # Every entity below needs at least one source_ref; fall back to a
            # catalog-level evidence unit built from purpose/when_to_use so the
            # record still carries real provenance instead of an empty list.
            fallback = self._add_evidence(
                id_parts=[catalog_id, "purpose"],
                text=purpose or title,
                source_id=source_id,
            )
            evidence_ids = [fallback.id]

        # The access surface itself becomes a `system` entity (it is the
        # thing operators/support interact with as a coherent surface).
        surface_entity = self.registry.get_or_create(
            EntityType.SYSTEM,
            access_surface,
            description=purpose,
            aliases=aliases,
            payload={"operational_roles": [], "owned_domains": [], "health_surfaces": []},
            source_refs=evidence_ids,
        )

        # architecture_notes[] and gaps[] are real, citable assertions about
        # the surface — e.g. "OPC path also connects hospital tags via
        # Ignition" — that were previously silently dropped (never even read
        # by this function). Both belong as Claims, not flattened into the
        # entity's own description, since they are arguable/supersedable
        # statements about the surface, not the surface's own definition.
        # gaps[] specifically maps onto polarity=uncertain: it is the
        # catalog author's own flagged incompleteness ("hospital HMI screen
        # dictionary thinner than tipper — needs expansion"), not a
        # confirmed fact, and should not be recorded as affirmed.
        for idx, note in enumerate(data.get("architecture_notes", [])):
            if not note:
                continue
            c_id = claim_id(f"{catalog_id}_architecture_note_{idx}", "has_architecture_note")
            self.claims[c_id] = Claim(
                id=c_id,
                subject_entity_id=surface_entity.id,
                predicate="has_architecture_note",
                object=LiteralValueObject(kind="literal", value=note),
                polarity=Polarity.AFFIRMED,
                source_refs=evidence_ids,
            )
        for idx, gap in enumerate(data.get("gaps", [])):
            if not gap:
                continue
            c_id = claim_id(f"{catalog_id}_gap_{idx}", "has_known_gap")
            self.claims[c_id] = Claim(
                id=c_id,
                subject_entity_id=surface_entity.id,
                predicate="has_known_gap",
                object=LiteralValueObject(kind="literal", value=gap),
                polarity=Polarity.UNCERTAIN,
                source_refs=evidence_ids,
            )
        # not_for[] was previously only read for capability_catalog.json;
        # surface catalogs carry their own not_for[] too (e.g. "Tipper VISU
        # screens" listed under hospital_hmi's not_for) and it was silently
        # dropped the same way architecture_notes/gaps were. negated polarity
        # is the correct shape here: it is an explicit "this does NOT apply"
        # assertion, not an affirmed fact about the surface.
        for idx, item in enumerate(data.get("not_for", [])):
            if not item:
                continue
            c_id = claim_id(f"{catalog_id}_not_for_{idx}", "not_applicable_to")
            self.claims[c_id] = Claim(
                id=c_id,
                subject_entity_id=surface_entity.id,
                predicate="not_applicable_to",
                object=LiteralValueObject(kind="literal", value=item),
                polarity=Polarity.NEGATED,
                source_refs=evidence_ids,
            )

        # screens_or_views -> ui_screen entities, displayed by the surface.
        # screen_entity_by_catalog_id tracks each screen's catalog-internal
        # `id` so the objects[] loop below can detect when an object entry
        # is the SAME screen cross-referenced a second time (see next
        # comment) rather than a distinct physical/API object.
        screen_entity_by_catalog_id: dict[str, Entity] = {}
        for screen in data.get("screens_or_views", []):
            screen_entity = self.registry.get_or_create(
                EntityType.UI_SCREEN,
                screen.get("title") or screen["id"],
                description=screen.get("purpose", ""),
                aliases=screen.get("aliases", []),
                payload={
                    "surface": access_surface,
                    "navigation_hint": [],
                    "visible_fields": [
                        {"name": point, "meaning": point} for point in screen.get("key_points", [])
                    ],
                    "artifact_ids": [],
                },
                source_refs=evidence_ids,
            )
            self._add_relationship(
                surface_entity.id,
                RelationshipType.DISPLAYS,
                screen_entity.id,
                source_refs=evidence_ids,
                note=f"{access_surface} displays {screen.get('title') or screen['id']}",
            )
            if screen.get("id"):
                screen_entity_by_catalog_id[screen["id"]] = screen_entity

        # objects -> component entities (DBs/APIs/hardware named at this
        # surface layer; the SQL catalog itself supplies the richer
        # database/database_table entities in migrate_wcs_sql_catalog).
        #
        # tipper_hmi_catalog.json lists each VISU_* screen in BOTH
        # screens_or_views[] and objects[] under the same catalog-internal
        # `id` (the objects[] entry even carries "kind": "visu_screen") —
        # found as a real duplicate (identical source_refs on both an
        # entity:ui_screen and an entity:component record) during a
        # duplicate-entity audit. When an object's id matches a screen
        # already created above, reuse that ui_screen entity instead of
        # creating a second component entity for the same real screen.
        for obj in data.get("objects", []):
            existing_screen = screen_entity_by_catalog_id.get(obj.get("id"))
            if existing_screen is not None:
                obj_entity = existing_screen
            else:
                obj_entity = self.registry.get_or_create(
                    EntityType.COMPONENT,
                    obj.get("label") or obj["id"],
                    aliases=obj.get("aliases", []),
                    source_refs=evidence_ids,
                )
            self._add_relationship(
                surface_entity.id,
                RelationshipType.USES,
                obj_entity.id,
                source_refs=evidence_ids,
            )
            for cap_slug in obj.get("capability_hints", []):
                cap = self._get_or_create_capability(cap_slug, source_refs=evidence_ids)
                self._add_relationship(
                    obj_entity.id,
                    RelationshipType.SUPPORTS,
                    cap.id,
                    source_refs=evidence_ids,
                )

        # activities -> capability records, plus their observables become
        # claims are deferred (Part 1 does not model observable-state claims
        # yet); the activity->capability and surface->capability edges are
        # what's needed for Capability.allowed_surface_entity_ids parity.
        for activity in data.get("activities", []):
            for cap_slug in activity.get("capability_hints", []):
                cap = self._get_or_create_capability(
                    cap_slug,
                    label=activity.get("label"),
                    source_refs=evidence_ids,
                )
                if surface_entity.id not in cap.allowed_surface_entity_ids:
                    updated = cap.model_copy(
                        update={
                            "allowed_surface_entity_ids": [
                                *cap.allowed_surface_entity_ids,
                                surface_entity.id,
                            ]
                        }
                    )
                    self.capabilities[updated.id] = updated

        # related_capabilities -> surface supports capability
        for cap_slug in data.get("related_capabilities", []):
            cap = self._get_or_create_capability(cap_slug, source_refs=evidence_ids)
            self._add_relationship(
                surface_entity.id,
                RelationshipType.SUPPORTS,
                cap.id,
                source_refs=evidence_ids,
            )

        # related_failure_patterns -> surface observes symptom
        for pattern_slug in data.get("related_failure_patterns", []):
            symptom = self._get_or_create_symptom(pattern_slug, source_refs=evidence_ids)
            self._add_relationship(
                surface_entity.id,
                RelationshipType.OBSERVES,
                symptom.id,
                source_refs=evidence_ids,
            )

    # -- capability catalog ------------------------------------------------

    def migrate_capability_catalog(self, data: dict[str, Any]) -> None:
        source_id = "catalog:capabilities"
        for cap in data.get("capabilities", []):
            cap_slug = cap["id"]
            evidence_ids: list[str] = []
            for idx, activity in enumerate(cap.get("activities", [])):
                unit = self._add_evidence(
                    id_parts=[cap_slug, "activity", str(idx)],
                    text=activity.get("action", activity.get("id", "")),
                    source_id=source_id,
                )
                evidence_ids.append(unit.id)
            if not evidence_ids:
                unit = self._add_evidence(
                    id_parts=[cap_slug, "job"],
                    text=cap.get("job", cap.get("description", cap_slug)),
                    source_id=source_id,
                )
                evidence_ids = [unit.id]

            target_entity_ids: list[str] = []
            for db in cap.get("primary_databases", []) + cap.get("secondary_databases", []):
                db_entity = self.registry.get_or_create(
                    EntityType.DATABASE,
                    db,
                    source_refs=evidence_ids,
                )
                target_entity_ids.append(db_entity.id)

            allowed_surface_ids: list[str] = []
            for surface in cap.get("primary_access_surfaces", []) + cap.get(
                "secondary_access_surfaces", []
            ):
                surface_entity = self.registry.resolve(EntityType.SYSTEM, surface)
                if surface_entity is None:
                    surface_entity = self.registry.get_or_create(
                        EntityType.SYSTEM,
                        surface,
                        source_refs=evidence_ids,
                    )
                allowed_surface_ids.append(surface_entity.id)

            required_role_ids: list[str] = []
            role_paths: list[RolePathGuidance] = []
            for role_name, guidance in (cap.get("role_paths") or {}).items():
                role_entity = self.registry.get_or_create(
                    EntityType.ROLE,
                    role_name,
                    source_refs=evidence_ids,
                )
                required_role_ids.append(role_entity.id)
                if isinstance(guidance, str) and guidance.strip():
                    role_paths.append(
                        RolePathGuidance(role_entity_id=role_entity.id, guidance=guidance.strip())
                    )

            # sql_model_links[].purpose and field_highlights are the field-
            # level "why" that field_highlights alone (bare names) loses;
            # both feed SqlFieldNote so a future reader knows not just which
            # table/field to check but what it's for. The referenced table
            # entity may not exist yet (wcs_sql_catalog migrates after this
            # method) — get_or_create still returns/creates a stable id, and
            # migrate_wcs_sql_catalog's later pass merges its richer payload
            # into the same entity by name. database_entity_id is filled from
            # the same database slug the catalog names (robotics, etc.).
            sql_field_notes: list[SqlFieldNote] = []
            for link in cap.get("sql_model_links", []):
                db_name = link.get("database") or "unknown"
                db_entity = self.registry.get_or_create(
                    EntityType.DATABASE,
                    db_name,
                    source_refs=evidence_ids,
                )
                table_entity = self.registry.get_or_create(
                    EntityType.DATABASE_TABLE,
                    link["model"],
                    payload={"database_name": db_name},
                    source_refs=evidence_ids,
                )
                sql_field_notes.append(
                    SqlFieldNote(
                        database_entity_id=db_entity.id,
                        table_entity_id=table_entity.id,
                        field=link["model"],
                        purpose=link.get("purpose") or "",
                    )
                )
            for highlight in cap.get("field_highlights", []):
                db_name = highlight.get("database") or "unknown"
                db_entity = self.registry.get_or_create(
                    EntityType.DATABASE,
                    db_name,
                    source_refs=evidence_ids,
                )
                table_entity = self.registry.get_or_create(
                    EntityType.DATABASE_TABLE,
                    highlight["model"],
                    payload={"database_name": db_name},
                    source_refs=evidence_ids,
                )
                # `meaning` can be explicit null (paired with needs_sme: true)
                # rather than absent — that is a real "not yet documented"
                # signal from the source catalog, not a missing key; preserve
                # it as an empty purpose rather than assuming a default.
                sql_field_notes.append(
                    SqlFieldNote(
                        database_entity_id=db_entity.id,
                        table_entity_id=table_entity.id,
                        field=highlight["field"],
                        purpose=highlight.get("meaning") or "",
                    )
                )

            observables_data = cap.get("observables") or {}
            observables = Observables(
                healthy=observables_data.get("healthy", []),
                degraded=observables_data.get("degraded", []),
                escalate=observables_data.get("escalate", []),
            )

            support_contract = None
            sc = cap.get("support_contract")
            if sc:
                diagnostic_ids = [
                    self.registry.get_or_create(EntityType.SYSTEM, s, source_refs=evidence_ids).id
                    for s in sc.get("diagnostic_surfaces", [])
                ]
                control_ids = [
                    self.registry.get_or_create(EntityType.SYSTEM, s, source_refs=evidence_ids).id
                    for s in sc.get("control_surfaces", [])
                ]
                required_evidence_ids = [capability_id(c) for c in sc.get("required_evidence", [])]
                forbidden_ids = [capability_id(c) for c in sc.get("forbidden_capabilities", [])]
                preferred = None
                mappings = sc.get("backend_mappings") or []
                if mappings and mappings[0].get("preferred_support_surface"):
                    preferred = self.registry.get_or_create(
                        EntityType.SYSTEM, mappings[0]["preferred_support_surface"], source_refs=evidence_ids
                    ).id
                support_contract = SupportContract(
                    diagnostic_surface_entity_ids=diagnostic_ids,
                    control_surface_entity_ids=control_ids,
                    required_evidence_capability_ids=required_evidence_ids,
                    forbidden_capability_ids=forbidden_ids,
                    preferred_surface_entity_id=preferred,
                )

            capability = Capability(
                id=capability_id(cap_slug),
                name=cap.get("label", cap_slug),
                description=cap.get("description", cap.get("job", "")),
                capability_kind=_capability_kind_for(cap_slug),
                when_to_use=[cap["when_to_use"]] if cap.get("when_to_use") else [],
                not_for=[cap["not_for"]] if cap.get("not_for") else [],
                target_entity_ids=target_entity_ids,
                allowed_surface_entity_ids=allowed_surface_ids,
                required_role_ids=required_role_ids,
                role_paths=role_paths,
                sql_field_notes=sql_field_notes,
                api_checks=cap.get("api_checks", []),
                observables=observables,
                support_contract=support_contract,
                source_refs=evidence_ids,
            )
            self.capabilities[capability.id] = capability
            self._capability_index[cap_slug] = capability.id

            for pattern_slug in cap.get("failure_patterns", []):
                symptom = self._get_or_create_symptom(pattern_slug, source_refs=evidence_ids)
                self._add_relationship(
                    symptom.id,
                    RelationshipType.MAY_INDICATE,
                    capability.id,
                    source_refs=evidence_ids,
                    note=f"{pattern_slug} may indicate a need to run {cap.get('label', cap_slug)}",
                )

        # SupportContract.required_evidence / forbidden_capabilities can name
        # a capability slug that has no card of its own in this catalog
        # (e.g. "ignition_restart" is referenced as forbidden but never
        # defined). Create a minimal stub for each so every id a
        # SupportContract points at resolves to a real record instead of a
        # well-formed but dangling reference.
        for cap in data.get("capabilities", []):
            sc = cap.get("support_contract") or {}
            for referenced_slug in [*sc.get("required_evidence", []), *sc.get("forbidden_capabilities", [])]:
                if referenced_slug not in self._capability_index:
                    self._get_or_create_capability(
                        referenced_slug,
                        source_refs=[
                            self._add_evidence(
                                id_parts=[referenced_slug, "referenced_only"],
                                text=(
                                    f"{referenced_slug} is referenced by other capabilities' support_contract "
                                    f"but has no capability card of its own in capability_catalog.json."
                                ),
                                source_id=source_id,
                            ).id
                        ],
                    )

    # -- wcs sql catalog -----------------------------------------------------

    def migrate_wcs_sql_catalog(self, data: dict[str, Any]) -> None:
        source_id = "catalog:wcs_sql"
        for db in data.get("databases", []):
            db_slug = db["id"]
            evidence_ids: list[str] = []
            for idx, item in enumerate(db.get("evidence", [])):
                unit = self._add_evidence(
                    id_parts=["database", db_slug, str(idx)],
                    text=item.get("snippet", ""),
                    source_id=item.get("source", source_id),
                )
                evidence_ids.append(unit.id)
            if not evidence_ids:
                unit = self._add_evidence(
                    id_parts=["database", db_slug, "purpose"],
                    text=db.get("purpose", db.get("label", db_slug)),
                    source_id=source_id,
                )
                evidence_ids = [unit.id]

            db_entity = self.registry.get_or_create(
                EntityType.DATABASE,
                db.get("label", db_slug),
                description=db.get("purpose", ""),
                aliases=db.get("aliases", []),
                source_refs=evidence_ids,
            )

        for model in data.get("models", []):
            model_name = model["name"]
            db_ref = model.get("database")
            evidence_ids = []
            key_fields = []
            for field_def in model.get("fields", []):
                key_fields.append(
                    {
                        "name": field_def["name"],
                        "meaning": field_def.get("meaning", field_def["name"]),
                    }
                )
                for idx, item in enumerate(field_def.get("evidence", [])):
                    unit = self._add_evidence(
                        id_parts=["model", model_name, field_def["name"], str(idx)],
                        text=item.get("snippet", ""),
                        source_id=item.get("source", source_id),
                    )
                    evidence_ids.append(unit.id)
            if not evidence_ids:
                unit = self._add_evidence(
                    id_parts=["model", model_name, "purpose"],
                    text=model.get("purpose", model_name),
                    source_id=source_id,
                )
                evidence_ids = [unit.id]

            table_entity = self.registry.get_or_create(
                EntityType.DATABASE_TABLE,
                model_name,
                description=model.get("purpose", ""),
                payload={
                    "database_name": db_ref or "unknown",
                    "schema_name": None,
                    "business_meanings": [],
                    "key_fields": key_fields,
                    "read_only": True,
                },
                source_refs=evidence_ids,
            )

            if db_ref:
                db_entity = self.registry.resolve(EntityType.DATABASE, db_ref)
                if db_entity is not None:
                    self._add_relationship(
                        db_entity.id,
                        RelationshipType.CONTAINS,
                        table_entity.id,
                        source_refs=evidence_ids,
                    )

            for cap_slug in model.get("capability_hints", []):
                cap = self._get_or_create_capability(cap_slug, source_refs=evidence_ids)
                updated_targets = list(dict.fromkeys([*cap.target_entity_ids, table_entity.id]))
                if updated_targets != cap.target_entity_ids:
                    cap = cap.model_copy(update={"target_entity_ids": updated_targets})
                    self.capabilities[cap.id] = cap
                self._add_relationship(
                    table_entity.id,
                    RelationshipType.SUPPORTS,
                    cap.id,
                    source_refs=evidence_ids,
                )

    # -- cross links -----------------------------------------------------

    def migrate_cross_links(self, data: dict[str, Any]) -> None:
        source_id = "catalog:cross_links"
        for edge in data.get("capability_failure_edges", []):
            cap_slug = edge["capability"]
            cap = self._get_or_create_capability(cap_slug)
            for pattern_slug in edge.get("failure_patterns", []):
                unit = self._add_evidence(
                    id_parts=["capability_failure_edge", cap_slug, pattern_slug],
                    text=f"{cap_slug} is cross-linked to failure pattern {pattern_slug}",
                    source_id=edge.get("source", source_id),
                )
                symptom = self._get_or_create_symptom(pattern_slug, source_refs=[unit.id])
                self._add_relationship(
                    symptom.id,
                    RelationshipType.MAY_INDICATE,
                    cap.id,
                    source_refs=[unit.id],
                )
                cap_with_ref = self.capabilities[cap.id]
                if unit.id not in cap_with_ref.source_refs:
                    updated = cap_with_ref.model_copy(
                        update={"source_refs": [*cap_with_ref.source_refs, unit.id]}
                    )
                    self.capabilities[updated.id] = updated

    # -- entrypoint -----------------------------------------------------

    def run(self) -> None:
        capability_catalog_path = CATALOGS_DIR / "capability_catalog.json"
        self.migrate_capability_catalog(json.loads(capability_catalog_path.read_text(encoding="utf-8")))

        wcs_sql_path = CATALOGS_DIR / "wcs_sql_catalog.json"
        self.migrate_wcs_sql_catalog(json.loads(wcs_sql_path.read_text(encoding="utf-8")))

        for filename in SURFACE_CATALOG_FILES:
            path = CATALOGS_DIR / filename
            self.migrate_surface_catalog(json.loads(path.read_text(encoding="utf-8")))

        cross_links_path = CATALOGS_DIR / "cross_links.json"
        self.migrate_cross_links(json.loads(cross_links_path.read_text(encoding="utf-8")))


def write_records(migration: CatalogMigration, output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)

    def dump(name: str, records: list) -> int:
        path = output_dir / f"{name}.json"
        payload = [json.loads(r.model_dump_json()) for r in records]
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return len(payload)

    counts = {
        "evidence_units": dump("evidence_units", list(migration.evidence_units.values())),
        "entities": dump("entities", migration.registry.all()),
        "capabilities": dump("capabilities", list(migration.capabilities.values())),
        "claims": dump("claims", list(migration.claims.values())),
        "relationships": dump("relationships", list(migration.relationships.values())),
    }
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to write brain/ record JSON bundles into (local-first storage).",
    )
    args = parser.parse_args()

    migration = CatalogMigration()
    migration.run()

    result = validate_batch(
        evidence_units=migration.evidence_units.values(),
        entities=migration.registry.all(),
        capabilities=migration.capabilities.values(),
        claims=migration.claims.values(),
        relationships=migration.relationships.values(),
    )
    if not result.valid:
        print(f"VALIDATION FAILED: {len(result.errors)} error(s)")
        for error in result.errors[:50]:
            print(f"  - {error}")
        raise SystemExit(1)

    counts = write_records(migration, args.output_dir)
    print("Ontology catalog migration complete.")
    for name, count in counts.items():
        print(f"  {name}: {count}")
    print(f"Written to: {args.output_dir}")


if __name__ == "__main__":
    main()
