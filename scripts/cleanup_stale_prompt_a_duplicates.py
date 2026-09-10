"""One-time cleanup: delete stale prompt_a playbook duplicates from a live Cosmos publish.

Root cause (fixed in shared_pipeline_stages/stage_11/corpus_merge.py,
_merge_playbooks_by_case): playbooks_prompt_a was merged by literal document id
across cumulative publishes instead of case_id, so every Stage 5 rerun that
changed a candidate's slug added a new playbook_id instead of replacing the
prior one for that case. publish_20260809_154541_a78f6e2a currently carries
14 stale prompt_a playbook_ids across the 4 published cases (see
data/output/cosmos_publish/prompt_a_duplicate_deprecations.json for the full
list, superseded_by mapping, and first-seen provenance).

This script deletes, for the CURRENTLY LIVE publish_version_id only:
  - the stale playbook document  (id = "playbook_{playbook_id}")
  - its embedding document       (id = "emb_playbook_prompt_a_{playbook_id}")
  - relationship_graph links whose source_record_id playbook segment matches
    a stale playbook_id (dangling playbook_runbook edges otherwise left behind)

It does NOT touch runbooks, other cases, other publish_version_id partitions,
or the kept/current playbook per case.

Usage:
    python scripts/cleanup_stale_prompt_a_duplicates.py --dry-run
    python scripts/cleanup_stale_prompt_a_duplicates.py --publish-version-id publish_20260809_154541_a78f6e2a --execute

Requires the same Cosmos env vars as the rest of Stage 11
(COSMOS_ENDPOINT, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER_*).
Nothing runs against Cosmos unless --execute is passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_11.cosmos_publisher import (  # noqa: E402
    _delete_document,
    load_cosmos_settings,
)

DEPRECATION_FILE = REPO_ROOT / "data/output/cosmos_publish/prompt_a_duplicate_deprecations.json"
RELATIONSHIP_SHARDS_DIR = REPO_ROOT / "data/output/cosmos_publish/publish_bundle/relationship_links"


def load_stale_playbook_ids() -> list[str]:
    data = json.loads(DEPRECATION_FILE.read_text(encoding="utf-8"))
    return [str(row["playbook_id"]) for row in data.get("deprecated", []) if row.get("playbook_id")]


def relationship_shard_ids_referencing(stale_ids: set[str]) -> list[str]:
    """Cosmos doc ids of relationship_graph shards that contain at least one
    link whose source_record_id references a stale playbook_id. Stage 11
    shards up to 2000 links per doc, so this identifies which shard DOCUMENTS
    need to be re-uploaded with the stale links filtered out (a shard is not
    deleted outright -- it also carries links for kept playbooks)."""
    hits: list[str] = []
    for shard_path in sorted(RELATIONSHIP_SHARDS_DIR.glob("shard_*.json")):
        shard = json.loads(shard_path.read_text(encoding="utf-8"))
        for link in shard.get("links", []):
            source = str(link.get("source_record_id") or "")
            playbook_part = source.split(":", 1)[0] if ":" in source else source
            if playbook_part in stale_ids:
                hits.append(str(shard.get("id") or shard_path.stem))
                break
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--publish-version-id",
        default="publish_20260809_154541_a78f6e2a",
        help="Live publish_version_id to clean up (partition key). Defaults to the currently live version.",
    )
    parser.add_argument("--execute", action="store_true", help="Actually delete from Cosmos. Omit for a dry run.")
    parser.add_argument("--dry-run", action="store_true", help="Explicit alias for the default (no --execute) behavior.")
    args = parser.parse_args()

    stale_ids = load_stale_playbook_ids()
    stale_id_set = set(stale_ids)
    print(f"Loaded {len(stale_ids)} stale playbook_ids from {DEPRECATION_FILE.relative_to(REPO_ROOT)}")
    for pid in stale_ids:
        print(f"  - {pid}")

    doc_ids = [f"playbook_{pid}" for pid in stale_ids]
    embedding_ids = [f"emb_playbook_prompt_a_{pid}" for pid in stale_ids]

    affected_shards = relationship_shard_ids_referencing(stale_id_set)
    print(f"\n{len(affected_shards)} relationship_graph shard(s) contain links to stale playbooks: {affected_shards}")
    print(
        "NOTE: shard documents are not deleted outright (they carry links for kept "
        "playbooks too). Re-run the normal cumulative publish after this cleanup and "
        "after the corpus_merge.py fix to regenerate clean shards, or filter+reupload "
        "manually if you need this resolved before the next publish."
    )

    if not args.execute:
        print(
            "\nDRY RUN (no --execute passed) -- nothing deleted. Would delete "
            f"{len(doc_ids)} playbook documents and {len(embedding_ids)} embedding "
            f"documents from publish_version_id={args.publish_version_id!r} in container "
            "COSMOS_CONTAINER_PLAYBOOKS_A."
        )
        for doc_id in doc_ids:
            print(f"  playbook doc:  {doc_id}")
        for emb_id in embedding_ids:
            print(f"  embedding doc: {emb_id}")
        return

    cosmos_settings = load_cosmos_settings()
    if not cosmos_settings.is_complete():
        raise RuntimeError(
            "Cosmos settings incomplete. Set COSMOS_ENDPOINT, COSMOS_KEY, COSMOS_DATABASE, "
            "and COSMOS_CONTAINER_* environment variables before running with --execute."
        )
    container = cosmos_settings.containers.get("playbooks_prompt_a")
    if not container:
        raise RuntimeError("No container mapping found for dataset 'playbooks_prompt_a'.")

    print(f"\nDeleting from container={container} publish_version_id={args.publish_version_id} ...")
    deleted = 0
    failures: list[str] = []
    for doc_id in [*doc_ids, *embedding_ids]:
        ok, warning = _delete_document(
            cosmos_settings=cosmos_settings,
            container=container,
            document_id=doc_id,
            publish_version_id=args.publish_version_id,
        )
        status = "deleted" if ok else "FAILED"
        print(f"  [{status}] {doc_id}" + (f" -- {warning}" if warning else ""))
        if ok:
            deleted += 1
        else:
            failures.append(doc_id)

    print(f"\n{deleted}/{len(doc_ids) + len(embedding_ids)} documents deleted.")
    if failures:
        print(f"Failed: {failures}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
