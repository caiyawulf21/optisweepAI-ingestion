"""Rewrite entity descriptions that leak source-reference language ("The
training slide presents...") into direct statements of fact.

This is the cosmetic-only tier from the entity-vs-claim audit (see
brain/migration/BRAIN_BUILD_PROCESS.md §6.7): the entity itself is correctly
modeled — only the description text needs a rewrite. No reclassification,
no relationship changes.

Two rewrite sources, applied in order:
1. entity_description_rewrites.REWRITES — hand-written, entity_id-keyed
   fixes for descriptions whose leak needs real sentence restructuring
   ("The X describes Y as Z" -> "Y is Z"). This is the PRIMARY path; most of
   this corpus needs it, not the mechanical one.
2. entity_shape.strip_source_reference_leak() — mechanical fallback for any
   OTHER leaked description not covered by the hand-written dict (e.g. a new
   source was migrated and produced a new leak). Only safely handles "The X
   states/notes/confirms that Y" -> "Y".

Since entity IDs are deterministic (content-derived, not random — see
brain/id_generation.py), a fresh Pass 0 -> Pass 1 -> consolidate -> Pass 1
rebuild reproduces the exact same entities with the exact same leaked
descriptions. Re-run this (with --write) after every fresh rebuild, the same
way reclassify_ambiguous_entities.py needs to be re-run for the 35
reclassified entities.

Run: python -m brain.migration.cleanup_entity_descriptions [--write]
"""

from __future__ import annotations

import argparse

from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.entity_description_rewrites import REWRITES
from brain.migration.entity_shape import LEAK_RE, strip_source_reference_leak
from brain.schemas.entity import Entity

ENTITIES_PATH = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs" / "entities.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    raw_entities = load_json(ENTITIES_PATH)

    hand_rewritten = 0
    mechanically_rewritten = 0
    unchanged_leaks = []
    updated = []
    for raw in raw_entities:
        desc = raw.get("description", "")
        if raw["id"] in REWRITES:
            new_desc = REWRITES[raw["id"]]
            if new_desc != desc:
                raw = {**raw, "description": new_desc}
                hand_rewritten += 1
        elif desc and LEAK_RE.search(desc):
            new_desc = strip_source_reference_leak(desc)
            if new_desc != desc:
                raw = {**raw, "description": new_desc}
                mechanically_rewritten += 1
            else:
                unchanged_leaks.append(raw["name"])
        updated.append(raw)

    print(f"Applied {hand_rewritten} hand-written rewrite(s) from entity_description_rewrites.py.")
    print(f"Mechanically rewrote {mechanically_rewritten} additional description(s).")
    if unchanged_leaks:
        print(f"{len(unchanged_leaks)} entity description(s) still leak source-reference language")
        print("but aren't in the hand-written dict and don't match a safely-strippable mechanical")
        print("pattern — likely new content from a source migrated after this file was last")
        print("updated. Review and add to entity_description_rewrites.REWRITES:")
        for n in unchanged_leaks[:20]:
            print(f"  - {n!r}")
        if len(unchanged_leaks) > 20:
            print(f"  ... and {len(unchanged_leaks) - 20} more")

    if not args.write:
        print("\nDRY RUN — nothing written. Pass --write to apply.")
        return

    dump_records([Entity.model_validate(e) for e in updated], ENTITIES_PATH)
    print(f"\nWrote {len(updated)} entities to {ENTITIES_PATH}")


if __name__ == "__main__":
    main()
