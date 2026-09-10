"""Provider-neutral Brain storage interface (newdesigndoc/
OPTISWEEP_BRAIN_API_NEUTRAL_AGENT_PLAN.md Step 2/4). brain_service calls
this, never a concrete backend, so local-JSON and (later) Azure Cosmos are
interchangeable without touching tool logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from brain.schemas.common import RecordType
from brain.validators import BrainRecordUnion


class StorageProvider(ABC):
    @abstractmethod
    def save_brain_records(self, records: list[BrainRecordUnion], *, scope: str) -> None:
        """Persist records into `scope` (e.g. "incidents/case_228086"),
        merging by id into whatever already exists there — never a blind
        overwrite of a populated scope."""

    @abstractmethod
    def load_brain_records(
        self, *, scope: str, record_type: RecordType | None = None
    ) -> list[BrainRecordUnion]:
        """Load records from one scope, optionally filtered to one record type."""

    @abstractmethod
    def load_brain_context(
        self,
        *,
        entity_ids: list[str] | None = None,
        record_type: RecordType | None = None,
    ) -> list[BrainRecordUnion]:
        """Load records across ALL scopes (Brain is source-agnostic), optionally
        filtered by record type and/or a set of ids to match against."""

    @abstractmethod
    def save_ingestion_run(self, run: dict[str, Any]) -> None:
        """Persist run/thread state for one ingestion job (must include a
        'run_id' key)."""

    @abstractmethod
    def load_ingestion_run(self, run_id: str) -> dict[str, Any] | None:
        """Load previously saved run state, or None if it doesn't exist."""

    @abstractmethod
    def save_embeddings(self, embeddings: list[dict[str, Any]]) -> None:
        """Persist a batch of embedding records, each shaped
        {"record_id": str, "record_type": str, "embedding_model": str,
        "vector": list[float]}. Upserts by record_id -- re-embedding an
        already-embedded record replaces its old vector, it does not
        duplicate it."""

    @abstractmethod
    def load_all_embeddings(self, record_type: RecordType | None = None) -> list[dict[str, Any]]:
        """Load every stored embedding, optionally filtered to one record
        type. Returns the same shape save_embeddings() accepts."""

    @abstractmethod
    def find_scope_for_record(self, record_id: str) -> str | None:
        """Return the scope a record with this id is ALREADY stored under
        (e.g. "ontology_catalogs" for a hand-curated Capability,
        "incidents/case_228086" for something from that case), or None if
        it doesn't exist anywhere yet. A merge (REINFORCE/PATCH) must write
        back to a record's own existing scope, never the scope of whatever
        new material triggered the merge -- saving under the wrong scope
        creates a second, divergent copy of the same id instead of
        updating the original (found as a real bug testing this live,
        2026-09-09: patching a shared ontology_catalogs Capability while
        ingesting a scratch test scope silently wrote a duplicate into the
        test scope, leaving the real record untouched)."""
