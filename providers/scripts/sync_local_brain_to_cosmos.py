"""One-way sync: push every record in the local Brain corpus
(brain/data/local/) into the live Azure Cosmos containers.

Idempotent -- AzureStorageProvider.save_brain_records() upserts by each
record's own content-derived id, so re-running this after a partial
failure or to pick up new local records never duplicates anything. Never
deletes from Cosmos; this is push-only.

Also syncs embeddings (save_embeddings/load_all_embeddings, a SEPARATE
corpus of vectors from the 7 BrainRecord types above -- get_brain_context's
semantic search reads these, not the record containers, so a
record-only sync leaves every query_text-based HTTP call
(/context/retrieve, /context/troubleshoot) returning zero matches against
Cosmos even though the records themselves are all there. Found by testing
the HTTP server live against azure storage after the first full sync
--this script originally pushed records only, confirmed via a live 200
OK / 0-excerpts response before this fix).

Usage:
    python -m providers.scripts.sync_local_brain_to_cosmos --dry-run
    python -m providers.scripts.sync_local_brain_to_cosmos --record-type capability
    python -m providers.scripts.sync_local_brain_to_cosmos
    python -m providers.scripts.sync_local_brain_to_cosmos --embeddings-only
"""

from __future__ import annotations

import argparse
import time

from brain.schemas.common import RecordType
from providers.azure_storage import AzureStorageProvider
from providers.local_storage import LocalStorageProvider

_BATCH_SIZE = 25


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Count what would be pushed without writing to Cosmos.")
    parser.add_argument(
        "--record-type",
        choices=[t.value for t in RecordType],
        help="Sync only this record type (e.g. capability). Default: all types.",
    )
    parser.add_argument(
        "--embeddings-only",
        action="store_true",
        help="Sync only embeddings, skipping the 7 BrainRecord containers entirely.",
    )
    parser.add_argument(
        "--missing-embeddings",
        action="store_true",
        help=(
            "Diff local vs. remote embeddings and push only what's missing from Cosmos, "
            "retrying harder (5 attempts, longer backoff) than the main sync's 1-retry "
            "policy -- for closing a gap left by an extended real outage, not a quick blip."
        ),
    )
    args = parser.parse_args()

    if args.missing_embeddings:
        _sync_missing_embeddings(dry_run=args.dry_run)
        return

    if args.embeddings_only:
        _sync_embeddings(dry_run=args.dry_run)
        return

    local = LocalStorageProvider()
    # Cosmos has no referential-integrity enforcement, so ordering here is
    # purely so a partial/interrupted run leaves the corpus in the most
    # useful partial state -- Entities/EvidenceUnits first since nearly
    # everything else (Claims, Relationships, Capabilities, Procedures,
    # Playbooks) cites one of these; Reviews last since they're
    # audit-trail records about the others, not referenced by anything.
    _DEPENDENCY_ORDER = [
        RecordType.ENTITY,
        RecordType.EVIDENCE_UNIT,
        RecordType.CLAIM,
        RecordType.RELATIONSHIP,
        RecordType.CAPABILITY,
        RecordType.PROCEDURE,
        RecordType.PLAYBOOK,
        RecordType.REVIEW,
    ]
    record_types = [RecordType(args.record_type)] if args.record_type else _DEPENDENCY_ORDER

    records_by_type = {
        record_type: [r for r in local.load_brain_context() if r.type == record_type]
        for record_type in record_types
    }
    # load_brain_context() scans the whole corpus once per call above --
    # cheap relative to network writes, and keeps this script a single
    # straightforward pass rather than threading a pre-filtered index
    # through (unlike brain_output_adapter.py's BrainCorpusIndex, this
    # script's own runtime is dominated by Cosmos round-trips, not local
    # corpus scans).

    total = sum(len(records) for records in records_by_type.values())
    print(f"Local corpus: {total} record(s) across {len(record_types)} type(s) selected for sync.")
    for record_type, records in records_by_type.items():
        print(f"  {record_type.value}: {len(records)}")

    if args.dry_run:
        print("\n--dry-run: nothing written to Cosmos.")
        if args.record_type is None:
            _sync_embeddings(dry_run=True)
        return

    if total == 0:
        print("\nNothing to sync.")
        return

    remote = AzureStorageProvider()
    pushed = 0
    failed: list[tuple[str, str]] = []
    started = time.monotonic()

    for record_type, records in records_by_type.items():
        for batch_start in range(0, len(records), _BATCH_SIZE):
            batch = records[batch_start : batch_start + _BATCH_SIZE]
            try:
                # scope is meaningless to AzureStorageProvider (partitions
                # by record content, not by caller-supplied scope -- see
                # its save_brain_records docstring), so any string works.
                remote.save_brain_records(batch, scope="local_sync")
                pushed += len(batch)
            except Exception as exc:  # noqa: BLE001 -- record and continue, don't abort a 20K-record run over one bad batch
                for record in batch:
                    failed.append((record.id, str(exc)))
            if pushed % 500 < _BATCH_SIZE:
                elapsed = time.monotonic() - started
                print(f"  ...{pushed}/{total} pushed ({elapsed:.0f}s elapsed)")

    elapsed = time.monotonic() - started
    print(f"\nDone: {pushed}/{total} pushed in {elapsed:.0f}s.")
    if failed:
        print(f"FAILED: {len(failed)} record(s). First 10:")
        for record_id, error in failed[:10]:
            print(f"  {record_id}: {error}")

    # Embeddings are a separate corpus from the 7 record types above --
    # always sync them too unless the caller asked for one --record-type
    # only, in which case a caller mid-troubleshooting a single type
    # probably doesn't want an unrelated embeddings pass tacked on.
    if args.record_type is None:
        _sync_embeddings(dry_run=False)


def _sync_embeddings(*, dry_run: bool) -> None:
    local = LocalStorageProvider()
    embeddings = local.load_all_embeddings()
    print(f"\nLocal embeddings: {len(embeddings)} vector(s) selected for sync.")
    if dry_run:
        print("--dry-run: nothing written to Cosmos.")
        return
    if not embeddings:
        print("Nothing to sync.")
        return

    remote = AzureStorageProvider()
    pushed = 0
    failed: list[tuple[str, str]] = []
    started = time.monotonic()
    for batch_start in range(0, len(embeddings), _BATCH_SIZE):
        batch = embeddings[batch_start : batch_start + _BATCH_SIZE]
        # A transient network failure (e.g. DNS resolution) partway
        # through a run this long must not abort the whole sync -- the
        # first real run hit exactly this after 2000/19766 pushed and
        # crashed with no retry, matching the record-sync loop above's
        # own catch-and-continue discipline (and the embedding backfill's
        # own precedent, per AGENT_DESIGN_NOTES.md: "hit one transient DNS
        # failure partway through and resumed correctly from where it left
        # off with zero duplicate work" -- upserts are idempotent, so a
        # simple re-run after a failure also works, but continuing past
        # one bad batch here means a single blip doesn't cost the whole
        # remaining run).
        for attempt in range(2):
            try:
                remote.save_embeddings(batch)
                pushed += len(batch)
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 0:
                    time.sleep(2)
                    continue
                for embedding in batch:
                    failed.append((embedding["record_id"], str(exc)))
        if pushed % 2000 < _BATCH_SIZE:
            elapsed = time.monotonic() - started
            print(f"  ...{pushed}/{len(embeddings)} embeddings pushed ({elapsed:.0f}s elapsed)")
    elapsed = time.monotonic() - started
    print(f"Done: {pushed}/{len(embeddings)} embeddings pushed in {elapsed:.0f}s.")
    if failed:
        print(f"FAILED: {len(failed)} embedding(s) after retry. First 10:")
        for record_id, error in failed[:10]:
            print(f"  {record_id}: {error}")


def _sync_missing_embeddings(*, dry_run: bool) -> None:
    local = LocalStorageProvider()
    remote = AzureStorageProvider()

    local_embeddings = local.load_all_embeddings()
    print(f"Local embeddings: {len(local_embeddings)}. Querying Cosmos for what's already there "
          "(a full cross-partition scan -- can take a few minutes at this corpus size)...")
    remote_ids = {e["record_id"] for e in remote.load_all_embeddings()}
    print(f"Remote embeddings: {len(remote_ids)}.")

    missing = [e for e in local_embeddings if e["record_id"] not in remote_ids]
    print(f"Missing from Cosmos: {len(missing)}.")
    if dry_run:
        print("--dry-run: nothing written to Cosmos.")
        return
    if not missing:
        print("Nothing to sync.")
        return

    pushed = 0
    failed: list[tuple[str, str]] = []
    started = time.monotonic()
    for embedding in missing:
        last_error = ""
        for attempt in range(5):
            try:
                remote.save_embeddings([embedding])
                pushed += 1
                last_error = ""
                break
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                time.sleep(min(2**attempt, 30))
        if last_error:
            failed.append((embedding["record_id"], last_error))
        if pushed % 25 == 0:
            elapsed = time.monotonic() - started
            print(f"  ...{pushed}/{len(missing)} pushed ({elapsed:.0f}s elapsed)")

    elapsed = time.monotonic() - started
    print(f"\nDone: {pushed}/{len(missing)} previously-missing embeddings pushed in {elapsed:.0f}s.")
    if failed:
        print(f"STILL FAILED after 5 attempts each: {len(failed)}. First 10:")
        for record_id, error in failed[:10]:
            print(f"  {record_id}: {error}")


if __name__ == "__main__":
    main()
