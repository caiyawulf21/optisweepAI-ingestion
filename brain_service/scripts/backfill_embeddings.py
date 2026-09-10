"""One-time (or resumable re-run) embedding backfill for the existing
Brain corpus. Embeds every record's embedding_text_for() text and persists
via storage.save_embeddings(). Idempotent: re-running only re-embeds
records not already present in storage (or all of them, with --force).

Usage:
    python -m brain_service.scripts.backfill_embeddings --backend local
    python -m brain_service.scripts.backfill_embeddings --backend azure
    python -m brain_service.scripts.backfill_embeddings --backend local --dry-run
"""

from __future__ import annotations

import argparse
import time

from brain.schemas.common import RecordType
from brain_service.embedding_text import embedding_text_for
from providers.azure_openai_embeddings import AzureOpenAIEmbeddingProvider
from providers.embeddings import EmbeddingProvider
from providers.storage import StorageProvider

_BATCH_SIZE = 100
# Embeddable record types -- BrainReview is excluded: its embedding_text_for
# rule exists for completeness but reviews are working/pending material,
# not corpus content a semantic search over "what does Brain know" should
# surface (see AGENT_DESIGN_NOTES.md's approved-knowledge distinction,
# the same reasoning ContextPacket.approved_knowledge already applies).
_EMBEDDABLE_TYPES = [
    RecordType.EVIDENCE_UNIT,
    RecordType.ENTITY,
    RecordType.CLAIM,
    RecordType.RELATIONSHIP,
    RecordType.CAPABILITY,
    RecordType.PROCEDURE,
    RecordType.PLAYBOOK,
]


def backfill_embeddings(
    embeddings: EmbeddingProvider,
    storage: StorageProvider,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> dict[str, int]:
    already_embedded: set[str] = set()
    if not force:
        already_embedded = {row["record_id"] for row in storage.load_all_embeddings()}

    counts: dict[str, int] = {}
    for record_type in _EMBEDDABLE_TYPES:
        records = storage.load_brain_context(record_type=record_type)
        pending = [r for r in records if force or r.id not in already_embedded]
        counts[record_type.value] = len(pending)
        if dry_run or not pending:
            continue

        for start in range(0, len(pending), _BATCH_SIZE):
            batch = pending[start : start + _BATCH_SIZE]
            texts = [embedding_text_for(record) for record in batch]
            vectors = embeddings.embed_texts(texts)
            storage.save_embeddings(
                [
                    {
                        "record_id": record.id,
                        "record_type": record_type.value,
                        "embedding_model": embeddings.embedding_model_id(),
                        "vector": vector,
                    }
                    for record, vector in zip(batch, vectors)
                ]
            )
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["local", "azure"], default="local")
    parser.add_argument("--force", action="store_true", help="Re-embed records that already have an embedding.")
    parser.add_argument("--dry-run", action="store_true", help="Report counts without calling the embedding API.")
    args = parser.parse_args()

    if args.backend == "local":
        from providers.local_storage import LocalStorageProvider

        storage: StorageProvider = LocalStorageProvider()
    else:
        from providers.azure_storage import AzureStorageProvider

        storage = AzureStorageProvider()

    provider = AzureOpenAIEmbeddingProvider()

    started = time.monotonic()
    counts = backfill_embeddings(provider, storage, force=args.force, dry_run=args.dry_run)
    elapsed = time.monotonic() - started

    action = "would embed" if args.dry_run else "embedded"
    for record_type_value, count in counts.items():
        print(f"{action} {count} {record_type_value} record(s)")
    print(f"total: {action} {sum(counts.values())} record(s) in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
