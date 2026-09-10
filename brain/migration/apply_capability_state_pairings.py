"""Apply the hand-judged state/symptom pairings from capability_state_pairings.py:

For each of the 27 real capabilities:
1. Create (or resolve to an existing) the paired state/symptom Entity.
2. Add a Relationship (VERIFIES or CONTROLS, per the judgment) from the
   capability to that entity.
3. Re-identify the capability: new id (capability:<new_id_suffix>), new
   label, corrected capability_kind. The OLD capability id is retired.
4. Rewrite every Relationship/reference elsewhere in the corpus that used
   the old capability id, so nothing dangles.

This is a one-time application of a judged (not mechanical) mapping — see
capability_state_pairings.py's own docstring for why each pairing is what
it is. Re-running this script is idempotent: if a capability's id already
matches its new_capability_id_suffix, it is skipped.

Run: python -m brain.migration.apply_capability_state_pairings [--write]
"""

from __future__ import annotations

import argparse
import json

from brain.id_generation import capability_id, entity_id, relationship_id
from brain.migration.capability_state_pairings import PAIRINGS, STUB_CAPABILITY_KIND_FIXES
from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.schemas.capability import Capability
from brain.schemas.entity import Entity, EntityType
from brain.schemas.relationship import Relationship, RelationshipType

CATALOGS_DIR = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs"
OPERATIONAL_SOURCES_DIR = REPO_ROOT / "brain" / "data" / "local" / "operational_sources"
SOURCES = [
    "manual_optisweep_om_v3",
    "training_video_day1",
    "training_video_day2",
    "active_agv_error_query_1",
    "video_training_inspection",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    entities_path = CATALOGS_DIR / "entities.json"
    capabilities_path = CATALOGS_DIR / "capabilities.json"

    raw_entities = load_json(entities_path)
    raw_capabilities = load_json(capabilities_path)
    entities_by_id = {e["id"]: e for e in raw_entities}
    capabilities_by_id = {c["id"]: c for c in raw_capabilities}

    new_entities: list[dict] = []
    new_relationships: list[dict] = []
    id_remap: dict[str, str] = {}  # old capability:<slug> -> new capability:<slug>
    updated_capabilities = 0
    skipped_already_applied = 0

    for old_slug, pairing in PAIRINGS.items():
        old_cap_id = capability_id(old_slug)
        new_cap_id = capability_id(pairing["new_capability_id_suffix"])

        if old_cap_id not in capabilities_by_id:
            if new_cap_id in capabilities_by_id:
                skipped_already_applied += 1
                # Already re-identified on a prior run — but old_cap_id may
                # still dangle elsewhere in the corpus (relationships that
                # weren't remapped by that earlier run), so keep registering
                # the remap even though there's no capability record left to
                # change here.
                id_remap[old_cap_id] = new_cap_id
                continue
            print(f"WARNING: capability {old_cap_id} not found, skipping")
            continue

        cap = dict(capabilities_by_id[old_cap_id])

        # 1. paired state/symptom entity
        state_type = pairing["state_entity_type"]
        state_name = pairing["state_entity_name"]
        entity_type_enum = EntityType(state_type)
        new_eid = entity_id(state_type, state_name)
        if new_eid not in entities_by_id:
            payload = {}
            entity_record = {
                "id": new_eid,
                "type": "entity",
                "schema_version": "1.0",
                "source_refs": list(cap.get("source_refs", [])),
                "constraints": {"sites": [], "product_versions": [], "environments": []},
                "created_at": cap.get("created_at"),
                "updated_at": cap.get("updated_at"),
                "entity_type": state_type,
                "name": state_name,
                "description": f"The condition {cap.get('name', old_slug)!r} is defined to check for.",
                "aliases": [],
                "payload": payload,
            }
            new_entities.append(entity_record)
            entities_by_id[new_eid] = entity_record

        # 2. relationship from capability's NEW id to the state entity
        rel_type = pairing["relationship_type"]
        rel_id = relationship_id(new_cap_id, rel_type, new_eid)
        new_relationships.append(
            {
                "id": rel_id,
                "type": "relationship",
                "schema_version": "1.0",
                "source_refs": list(cap.get("source_refs", []))[:5] or [old_cap_id],
                "constraints": {"sites": [], "product_versions": [], "environments": []},
                "created_at": cap.get("created_at"),
                "updated_at": cap.get("updated_at"),
                "from_id": new_cap_id,
                "relationship_type": rel_type,
                "to_id": new_eid,
                "note": f"{pairing['new_capability_label']} {rel_type} {state_name}",
            }
        )

        # 3. re-identify the capability
        cap["id"] = new_cap_id
        cap["name"] = pairing["new_capability_label"]
        cap["capability_kind"] = pairing["capability_kind"]
        del capabilities_by_id[old_cap_id]
        capabilities_by_id[new_cap_id] = cap
        id_remap[old_cap_id] = new_cap_id
        updated_capabilities += 1

    # Stub capability_kind fixes (§6.12): these capabilities are never
    # re-identified (their id/label are already correct), only their
    # capability_kind is wrong. Applied directly, not through id_remap.
    stub_kind_fixes_applied = 0
    for slug, correct_kind in STUB_CAPABILITY_KIND_FIXES.items():
        cid = capability_id(slug)
        cap = capabilities_by_id.get(cid)
        if cap is None:
            print(f"WARNING: stub capability {cid} not found, skipping kind fix")
            continue
        if cap.get("capability_kind") != correct_kind:
            cap["capability_kind"] = correct_kind
            stub_kind_fixes_applied += 1

    # support_contract.{required_evidence_capability_ids,forbidden_capability_ids}
    # are internal capability-to-capability references and must also be
    # remapped, or they dangle even though validate_batch() doesn't check them.
    support_contract_refs_updated = 0
    for cap in capabilities_by_id.values():
        sc = cap.get("support_contract")
        if not sc:
            continue
        for field in ("required_evidence_capability_ids", "forbidden_capability_ids"):
            ids = sc.get(field) or []
            new_ids = [id_remap.get(cid, cid) for cid in ids]
            if new_ids != ids:
                sc[field] = new_ids
                support_contract_refs_updated += sum(1 for a, b in zip(ids, new_ids) if a != b)

    print(f"Capabilities re-identified: {updated_capabilities}")
    print(f"Already applied (skipped): {skipped_already_applied}")
    print(f"New state/symptom entities: {len(new_entities)}")
    print(f"New VERIFIES/CONTROLS relationships: {len(new_relationships)}")
    if support_contract_refs_updated:
        print(f"support_contract capability references remapped: {support_contract_refs_updated}")
    if stub_kind_fixes_applied:
        print(f"Stub capability_kind fixes applied: {stub_kind_fixes_applied}")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        for old, new in id_remap.items():
            print(f"  {old} -> {new}")
        return

    # Write entities.json (existing + new)
    all_entities = [Entity.model_validate(e) for e in entities_by_id.values()]
    dump_records(all_entities, entities_path)
    print(f"Wrote {len(all_entities)} entities to {entities_path}")

    # Write capabilities.json (re-identified)
    all_capabilities = [Capability.model_validate(c) for c in capabilities_by_id.values()]
    dump_records(all_capabilities, capabilities_path)
    print(f"Wrote {len(all_capabilities)} capabilities to {capabilities_path}")

    # Existing catalog relationships (e.g. may_indicate/supports -> capability)
    # also reference old capability ids and must be remapped BEFORE combining
    # with the newly-created VERIFIES/CONTROLS relationships.
    relationships_path = CATALOGS_DIR / "relationships.json"
    existing_relationships = load_json(relationships_path) if relationships_path.exists() else []
    catalog_changed = 0
    for r in existing_relationships:
        if r["from_id"] in id_remap:
            r["from_id"] = id_remap[r["from_id"]]
            catalog_changed += 1
        if r["to_id"] in id_remap:
            r["to_id"] = id_remap[r["to_id"]]
            catalog_changed += 1
    if catalog_changed:
        print(f"ontology_catalogs: updated {catalog_changed} relationship endpoint(s) to new capability ids")

    combined = existing_relationships + new_relationships
    dump_records([Relationship.model_validate(r) for r in combined], relationships_path)
    print(f"Wrote {len(combined)} relationships to {relationships_path}")

    # Rewrite every other reference to an old capability id across the corpus
    for source in SOURCES:
        rels_path = OPERATIONAL_SOURCES_DIR / source / "relationships.json"
        if not rels_path.exists():
            continue
        rels = load_json(rels_path)
        changed = 0
        for r in rels:
            if r["from_id"] in id_remap:
                r["from_id"] = id_remap[r["from_id"]]
                changed += 1
            if r["to_id"] in id_remap:
                r["to_id"] = id_remap[r["to_id"]]
                changed += 1
        if changed:
            dump_records([Relationship.model_validate(r) for r in rels], rels_path)
            print(f"{source}: updated {changed} relationship endpoint(s) to new capability ids")


if __name__ == "__main__":
    main()
