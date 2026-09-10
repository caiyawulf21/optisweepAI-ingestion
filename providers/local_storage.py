"""Local-JSON implementation of StorageProvider, reading/writing the exact
existing brain/data/local/<scope>/<type_plural>.json layout that
brain/migration/ already produced during the backfill (Part 1 §10.3:
local mode must keep working with no Azure credentials).

Entity filenames are historically inconsistent across already-migrated
cases (entities.json in some, new_entities.json in others, absent in
others) -- both are read if present; entities.json is always written going
forward.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from brain.schemas.capability import Capability
from brain.schemas.claim import Claim
from brain.schemas.common import RecordType
from brain.schemas.entity import Entity
from brain.schemas.evidence_unit import EvidenceUnit
from brain.schemas.playbook import Playbook
from brain.schemas.procedure import Procedure
from brain.schemas.relationship import Relationship
from brain.schemas.review import BrainReview
from brain.validators import BrainRecordUnion
from providers.storage import StorageProvider

DEFAULT_LOCAL_ROOT = Path(__file__).resolve().parents[1] / "brain" / "data" / "local"

_MODEL_BY_TYPE: dict[RecordType, type[BrainRecordUnion]] = {
    RecordType.EVIDENCE_UNIT: EvidenceUnit,
    RecordType.ENTITY: Entity,
    RecordType.CLAIM: Claim,
    RecordType.RELATIONSHIP: Relationship,
    RecordType.CAPABILITY: Capability,
    RecordType.PROCEDURE: Procedure,
    RecordType.PLAYBOOK: Playbook,
    RecordType.REVIEW: BrainReview,
}

_FILENAME_BY_TYPE: dict[RecordType, str] = {
    RecordType.EVIDENCE_UNIT: "evidence_units.json",
    RecordType.ENTITY: "entities.json",
    RecordType.CLAIM: "claims.json",
    RecordType.RELATIONSHIP: "relationships.json",
    RecordType.CAPABILITY: "capabilities.json",
    RecordType.PROCEDURE: "procedures.json",
    RecordType.PLAYBOOK: "playbooks.json",
    RecordType.REVIEW: "reviews.json",
}

# Historical alternate filenames still present in already-migrated scopes,
# read as a fallback when the canonical name above doesn't exist.
_LEGACY_FILENAMES: dict[RecordType, tuple[str, ...]] = {
    RecordType.ENTITY: ("new_entities.json",),
}

_INGESTION_RUNS_DIRNAME = "ingestion_runs"
_EMBEDDINGS_DIRNAME = "embeddings"


class LocalStorageProvider(StorageProvider):
    def __init__(self, root: Path | str = DEFAULT_LOCAL_ROOT) -> None:
        self.root = Path(root)
        # Process-lifetime embedding cache: load_all_embeddings() re-reads
        # every embeddings/<type>.json file from disk on every call, which
        # measured ~6s for a cross-type query against ~9K vectors -- real
        # cost for a long-lived MCP server process to pay on every
        # semantic-search tool call. Cached here per record-type-key
        # (None = "all types"), invalidated by save_embeddings() so a
        # backfill or new ingestion is never served stale.
        self._embeddings_cache: dict[str | None, list[dict[str, Any]]] = {}

    # -- Brain records -----------------------------------------------------

    def save_brain_records(self, records: list[BrainRecordUnion], *, scope: str) -> None:
        if not records:
            return
        by_type: dict[RecordType, list[BrainRecordUnion]] = {}
        for record in records:
            by_type.setdefault(record.type, []).append(record)

        for record_type, new_records in by_type.items():
            path = self._path_for(scope, record_type)
            existing = self._load_file(path, record_type)
            by_id = {record.id: record for record in existing}
            for record in new_records:
                by_id[record.id] = record
            self._write_file(path, list(by_id.values()))

    def load_brain_records(
        self, *, scope: str, record_type: RecordType | None = None
    ) -> list[BrainRecordUnion]:
        types = [record_type] if record_type is not None else list(_MODEL_BY_TYPE)
        records: list[BrainRecordUnion] = []
        for one_type in types:
            records.extend(self._load_file(self._path_for(scope, one_type), one_type))
        return records

    def load_brain_context(
        self,
        *,
        entity_ids: list[str] | None = None,
        record_type: RecordType | None = None,
    ) -> list[BrainRecordUnion]:
        types = [record_type] if record_type is not None else list(_MODEL_BY_TYPE)
        wanted_ids = set(entity_ids) if entity_ids else None
        records: list[BrainRecordUnion] = []
        if not self.root.exists():
            return records
        for scope_dir in sorted(self._iter_scope_dirs()):
            scope = self._scope_for_dir(scope_dir)
            for one_type in types:
                for record in self._load_file(self._path_for(scope, one_type), one_type):
                    if wanted_ids is not None and record.id not in wanted_ids:
                        continue
                    records.append(record)
        return records

    def find_scope_for_record(self, record_id: str) -> str | None:
        if not self.root.exists():
            return None
        for scope_dir in sorted(self._iter_scope_dirs()):
            scope = self._scope_for_dir(scope_dir)
            for one_type in _MODEL_BY_TYPE:
                path = self._path_for(scope, one_type)
                if not path.exists() and not any(
                    path.with_name(name).exists() for name in _LEGACY_FILENAMES.get(one_type, ())
                ):
                    continue
                # A cheap raw-JSON id scan avoids fully validating every
                # record in every file just to check for one id's
                # presence -- this is called once per merge candidate, not
                # once per corpus load, so it's worth being deliberately
                # lighter than _load_file's full pydantic parse.
                raw_path = path if path.exists() else next(
                    (path.with_name(name) for name in _LEGACY_FILENAMES.get(one_type, ()) if path.with_name(name).exists()),
                    path,
                )
                raw = json.loads(raw_path.read_text(encoding="utf-8"))
                if any(row.get("id") == record_id for row in raw):
                    return scope
        return None

    def _iter_scope_dirs(self) -> list[Path]:
        """Every directory under root that directly contains at least one
        record JSON file, excluding the ingestion_runs bookkeeping dir.
        Scopes may be nested (e.g. "incidents/case_228086"), so this walks
        recursively rather than assuming a fixed depth."""
        known_filenames = set(_FILENAME_BY_TYPE.values())
        for names in _LEGACY_FILENAMES.values():
            known_filenames.update(names)
        excluded_top_level_dirs = {_INGESTION_RUNS_DIRNAME, _EMBEDDINGS_DIRNAME}
        scope_dirs: list[Path] = []
        for path in self.root.rglob("*"):
            if not path.is_dir():
                continue
            if excluded_top_level_dirs.intersection(path.relative_to(self.root).parts):
                continue
            if any((path / name).exists() for name in known_filenames):
                scope_dirs.append(path)
        return scope_dirs

    # -- Ingestion runs ------------------------------------------------------

    def save_ingestion_run(self, run: dict[str, Any]) -> None:
        run_id = run.get("run_id")
        if not run_id:
            raise ValueError("save_ingestion_run requires a 'run_id' key")
        path = self.root / _INGESTION_RUNS_DIRNAME / f"{run_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_ingestion_run(self, run_id: str) -> dict[str, Any] | None:
        path = self.root / _INGESTION_RUNS_DIRNAME / f"{run_id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    # -- Embeddings ------------------------------------------------------------
    # Stored corpus-wide (one file per record type under embeddings/), not
    # per-scope like Brain records -- a vector search query is inherently
    # corpus-wide (find the closest match anywhere), unlike
    # load_brain_records' scope-bounded lookup.

    def save_embeddings(self, embeddings: list[dict[str, Any]]) -> None:
        if not embeddings:
            return
        by_type: dict[str, list[dict[str, Any]]] = {}
        for embedding in embeddings:
            by_type.setdefault(embedding["record_type"], []).append(embedding)

        for record_type_value, new_embeddings in by_type.items():
            path = self.root / _EMBEDDINGS_DIRNAME / f"{record_type_value}.json"
            existing = self._load_embeddings_file(path)
            by_record_id = {e["record_id"]: e for e in existing}
            for embedding in new_embeddings:
                by_record_id[embedding["record_id"]] = embedding
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(list(by_record_id.values()), ensure_ascii=False), encoding="utf-8")

        # Invalidate the whole cache rather than trying to patch it in
        # place -- simplest correct behavior, and save_embeddings is called
        # in batches (a backfill run, or one ingestion event), not so often
        # that a full-cache clear is a real cost next to the disk I/O it's
        # already doing.
        self._embeddings_cache.clear()

    def load_all_embeddings(self, record_type: RecordType | None = None) -> list[dict[str, Any]]:
        cache_key = record_type.value if record_type is not None else None
        if cache_key in self._embeddings_cache:
            return self._embeddings_cache[cache_key]

        embeddings_dir = self.root / _EMBEDDINGS_DIRNAME
        if not embeddings_dir.exists():
            results: list[dict[str, Any]] = []
        else:
            types = [record_type.value] if record_type is not None else [t.value for t in _MODEL_BY_TYPE]
            results = []
            for type_value in types:
                results.extend(self._load_embeddings_file(embeddings_dir / f"{type_value}.json"))

        self._embeddings_cache[cache_key] = results
        return results

    def _load_embeddings_file(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    # -- internals -----------------------------------------------------------

    def _path_for(self, scope: str, record_type: RecordType) -> Path:
        return self.root / scope / _FILENAME_BY_TYPE[record_type]

    def _scope_for_dir(self, scope_dir: Path) -> str:
        return str(scope_dir.relative_to(self.root)).replace("\\", "/")

    def _load_file(self, path: Path, record_type: RecordType) -> list[BrainRecordUnion]:
        candidates = [path]
        if not path.exists():
            candidates.extend(path.with_name(name) for name in _LEGACY_FILENAMES.get(record_type, ()))
        for candidate in candidates:
            if candidate.exists():
                raw = json.loads(candidate.read_text(encoding="utf-8"))
                model = _MODEL_BY_TYPE[record_type]
                adapter: TypeAdapter[Any] = TypeAdapter(list[model])  # type: ignore[valid-type]
                return adapter.validate_python(raw)
        return []

    def _write_file(self, path: Path, records: list[BrainRecordUnion]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [record.model_dump(mode="json") for record in records]
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
