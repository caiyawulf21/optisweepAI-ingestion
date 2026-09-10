"""Post-hoc entity consolidation: merge near-duplicate entities created when
different sources name the same real-world thing slightly differently
(e.g. "OptiSweep WCS" vs "Fortna WCS" vs "WCS").

Why this is a separate pass, not built into EntityRegistry.resolve()
---------------------------------------------------------------------
EntityRegistry.resolve() only matches by exact slugified name/alias, by
design — Pass 0/1 migration should never guess that two differently-named
things are the same thing while it's still constructing the graph, because a
wrong merge during migration silently loses the distinction forever with no
review step. This script runs AFTER migration, is idempotent, and its merge
decisions are printed so they can be inspected before being trusted.

The matching rule (deliberately narrow, not generic fuzzy matching)
---------------------------------------------------------------------
Two entities of the SAME entity_type merge only when their names produce the
EXACTLY EQUAL token set once the two known brand words ("optisweep",
"fortna") are stripped — not substring overlap, not a similarity score. This
catches "OptiSweep WCS" / "Fortna WCS" / "WCS" (all -> {wcs}) and "OptiSweep
Tipper Subsystem" / "Tipper subsystem" (both -> {tipper, subsystem}), while
correctly refusing to merge "hospital" with "hospital module" (different
token sets: {hospital} vs {hospital, module}) since a bare concept and a
named software module are not guaranteed to be the same referent. Run this
script's report and read the merge list before trusting it on a new corpus;
it is intentionally conservative rather than maximally aggressive.

Run: python -m brain.migration.consolidate_entities
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from brain.migration.common import REPO_ROOT, dump_records, load_json
from brain.migration.merge import merge_record
from brain.schemas.entity import Entity

DEFAULT_ENTITIES_PATH = REPO_ROOT / "brain" / "data" / "local" / "ontology_catalogs" / "entities.json"

BRAND_WORDS = {"optisweep", "fortna"}

# Common nouns that are too generic to safely identify a merge candidate on
# their own — "system"/"module"/"software" appear as the ENTIRE remaining
# name for many genuinely different things once brand words are stripped
# ("OptiSweep system" the whole platform vs. some other bare "system"
# mention), so a lone occurrence of one of these must not trigger a merge.
# A short, acronym-shaped identifier like "WCS" or "RMS" is exactly the
# opposite case — specific enough on its own — so it is NOT in this set.
GENERIC_SINGLE_WORDS = {"system", "module", "subsystem", "service", "software", "robot"}


def core_tokens(name: str) -> frozenset[str] | None:
    """Return the name's brand-stripped token set, or None if the name isn't
    a safe candidate for this matching rule at all.

    Guards beyond brand-word stripping:
    - Any purely-numeric token (e.g. "1", "2" from "page_2_image_1") is
      rejected outright rather than dropped: token-SET equality is blind to
      order, so "page 2 image 1" and "page 1 image 2" would otherwise
      collide onto the same key despite being different referents. A name
      containing digits needs a smarter (order-aware) comparison this script
      does not attempt, so it opts out of matching entirely instead of
      matching wrong.
    - A token set that is empty, or is a single generic word
      (GENERIC_SINGLE_WORDS), is rejected: too weak a signal alone. A
      single SPECIFIC word (an acronym like "wcs", or any word not in
      GENERIC_SINGLE_WORDS) is accepted — that is exactly what makes "WCS"
      itself mergeable while "system" alone is not.
    """
    words = re.findall(r"[a-z0-9]+", name.lower())
    if any(w.isdigit() for w in words):
        return None
    tokens = frozenset(w for w in words if w not in BRAND_WORDS)
    if not tokens:
        return None
    if len(tokens) == 1 and next(iter(tokens)) in GENERIC_SINGLE_WORDS:
        return None
    return tokens


def find_merge_groups(entities: list[Entity]) -> dict[tuple[str, frozenset[str]], list[Entity]]:
    groups: dict[tuple[str, frozenset[str]], list[Entity]] = defaultdict(list)
    for entity in entities:
        key_tokens = core_tokens(entity.name)
        if key_tokens is None:
            continue
        groups[(entity.entity_type.value, key_tokens)].append(entity)
    return {key: members for key, members in groups.items() if len(members) > 1}


def _looks_garbled(name: str) -> bool:
    """Flag a name whose words repeat themselves (e.g. "...control system
    bag out" after "...system bag out control") — a duplicated-extraction
    artifact, not a more specific real name. Used to avoid picking a garbled
    name as the merge survivor just because it happens to be longer.
    """
    words = re.findall(r"[a-z0-9]+", name.lower())
    return len(words) >= 4 and len(set(words)) < len(words) * 0.75


def consolidate(entities: list[Entity]) -> tuple[list[Entity], list[dict]]:
    groups = find_merge_groups(entities)
    by_id = {e.id: e for e in entities}
    merge_log: list[dict] = []

    for (entity_type, _tokens), members in groups.items():
        # Prefer the longest non-garbled name as the canonical survivor (more
        # specific/branded names are usually longer), but never let a
        # duplicated-word extraction artifact win just for being longer.
        # Fold the others in via merge_record so aliases/source_refs/payload/
        # description all accumulate rather than being discarded, then drop
        # the losers from the id-keyed map.
        members_sorted = sorted(
            members, key=lambda e: (not _looks_garbled(e.name), len(e.name)), reverse=True
        )
        canonical = members_sorted[0]
        for loser in members_sorted[1:]:
            canonical = merge_record(
                canonical,
                {
                    "aliases": [loser.name, *loser.aliases],
                    "description": loser.description,
                    "source_refs": loser.source_refs,
                    "payload": loser.payload,
                },
            )
            del by_id[loser.id]
            merge_log.append(
                {
                    "entity_type": entity_type,
                    "merged_id": loser.id,
                    "merged_name": loser.name,
                    "into_id": canonical.id,
                    "into_name": canonical.name,
                }
            )
        by_id[canonical.id] = canonical

    return list(by_id.values()), merge_log


def _rewrite_references(entities: list[Entity], id_remap: dict[str, str]) -> list[Entity]:
    """Rewrite any UiScreenPayload.artifact_ids-style self-references that
    pointed at a now-merged entity id. Entities generally reference other
    entities only through Relationship records (out of scope here — see
    the module docstring); this covers the one payload-internal exception.
    """
    if not id_remap:
        return entities
    rewritten = []
    for entity in entities:
        payload = entity.payload
        if hasattr(payload, "artifact_ids") and payload.artifact_ids:
            new_ids = [id_remap.get(a, a) for a in payload.artifact_ids]
            if new_ids != payload.artifact_ids:
                entity = entity.model_copy(update={"payload": payload.model_copy(update={"artifact_ids": new_ids})})
        rewritten.append(entity)
    return rewritten


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entities-in", type=Path, default=DEFAULT_ENTITIES_PATH)
    parser.add_argument("--entities-out", type=Path, default=None, help="Default: overwrite --entities-in.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the merge plan without writing any changes."
    )
    args = parser.parse_args()

    raw_entities = load_json(args.entities_in)
    entities = [Entity.model_validate(r) for r in raw_entities]
    print(f"Loaded {len(entities)} entities from {args.entities_in}")

    merged_entities, merge_log = consolidate(entities)

    print(f"\nMerge plan: {len(merge_log)} entities merged into {len({m['into_id'] for m in merge_log})} survivors")
    for entry in merge_log:
        print(f"  [{entry['entity_type']}] {entry['merged_name']!r} ({entry['merged_id']}) -> {entry['into_name']!r} ({entry['into_id']})")

    if args.dry_run:
        print("\n--dry-run: no files written.")
        return

    id_remap = {m["merged_id"]: m["into_id"] for m in merge_log}
    merged_entities = _rewrite_references(merged_entities, id_remap)

    out_path = args.entities_out or args.entities_in
    count = dump_records(merged_entities, out_path)
    print(f"\nWrote {count} consolidated entities to {out_path}")

    if id_remap:
        remap_path = out_path.parent / "entity_consolidation_remap.json"
        remap_path.write_text(json.dumps(id_remap, indent=2), encoding="utf-8")
        print(f"Wrote id remap ({len(id_remap)} entries) to {remap_path}")
        print(
            "NOTE: Relationship/Claim/Capability records elsewhere still reference the merged-away ids. "
            "Re-run the source migrations (they re-resolve by name against the consolidated registry) "
            "rather than hand-patching those records."
        )


if __name__ == "__main__":
    main()
