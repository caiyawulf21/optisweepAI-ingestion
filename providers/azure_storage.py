"""Azure Cosmos DB implementation of StorageProvider, targeting Brain's own
containers (providers/azure_cosmos_config.py), NOT the pre-Brain publish
containers shared_pipeline_stages/stage_11/cosmos_publisher.py writes to.

The raw-REST Cosmos mechanics (HMAC-SHA256 master-key auth, upsert via
x-ms-documentdb-is-upsert, partition-scoped query/delete) are the same
approach cosmos_publisher.py already uses -- reimplemented here as a
small, self-contained module rather than importing that module's private
(_-prefixed) helpers, since this provider targets a structurally
different container/partition-key shape and has no other reason to
depend on that module's internals.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.parse
import urllib.request
from email.utils import formatdate
from typing import Any

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
from providers.azure_cosmos_config import (
    CONTAINER_BY_RECORD_TYPE,
    EMBEDDINGS_CONTAINER,
    INGESTION_RUNS_CONTAINER,
    BrainCosmosSettings,
    load_brain_cosmos_settings,
    partition_key_value,
)
from providers.storage import StorageProvider

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

_API_VERSION = "2018-12-31"
_TIMEOUT_SECONDS = 60

# Cosmos adds these to every stored document, and this repo's own
# `_partition_key` is added at write time only to satisfy the container's
# declared partition key path (see azure_cosmos_config.COSMOS_PARTITION_KEY_PATH) --
# none of them are real Brain schema fields, and every BrainRecord uses
# ConfigDict(extra="forbid"), so reading a document back without stripping
# these first fails validation on every single read.
_COSMOS_SYSTEM_FIELDS = frozenset({"_rid", "_self", "_etag", "_attachments", "_ts", "_partition_key"})


def _strip_cosmos_fields(document: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in document.items() if key not in _COSMOS_SYSTEM_FIELDS}


class AzureCosmosStorageError(RuntimeError):
    pass


class AzureStorageProvider(StorageProvider):
    """`scope` is accepted for interface compatibility with
    LocalStorageProvider but is NOT how Cosmos partitions records -- a
    Brain record's partition key is always derived from its own content
    (partition_key_value()), matching Part 1 §10.2's container plan, not
    from an ingestion-time directory grouping. save_brain_records/
    load_brain_records still take `scope` because StorageProvider's
    interface is shared by both backends; here it is used only to compute
    which EvidenceUnit.source_id-style records logically belong to it when
    filtering, mirroring LocalStorageProvider's own scope semantics as
    closely as a partition-keyed store allows."""

    def __init__(self, settings: BrainCosmosSettings | None = None) -> None:
        self.settings = settings or load_brain_cosmos_settings()
        if not self.settings.is_complete():
            raise RuntimeError(
                "Azure Cosmos is not configured for Brain storage. Set COSMOS_ENDPOINT, "
                "COSMOS_KEY, and COSMOS_DATABASE (shared with the existing pre-Brain "
                "publish path) -- Brain's own container names default automatically."
            )
        # Process-lifetime caches -- see LocalStorageProvider's identical
        # cache for the rationale (a cross-partition Cosmos query pays
        # network round-trips per page on every call otherwise, the same
        # class of repeated cost the local disk-read cache addresses).
        self._embeddings_cache: dict[str | None, list[dict[str, Any]]] = {}
        # Keyed by record type -- load_brain_context/load_brain_records both
        # route through _query_container per type, and every one of
        # get_brain_context's calls (entity lookup, per-hop relationship
        # scan, claim scan) previously re-fetched its ENTIRE container from
        # scratch with no caching at all, unlike load_all_embeddings above.
        # This was the dominant real cost in production (2026-09-10, found
        # via direct latency measurement against the deployed HTTP API):
        # a single /context/retrieve call could trigger 3-4 full,
        # uncached container scans (11,597 relationships alone) on top of
        # the embeddings cost this module already addressed.
        self._records_cache: dict[RecordType, list[BrainRecordUnion]] = {}

    # -- Brain records -----------------------------------------------------

    def save_brain_records(self, records: list[BrainRecordUnion], *, scope: str) -> None:
        del scope  # Cosmos partitions by the record's own content, not by scope; see class docstring.
        for record in records:
            container = self._container_for(record.type)
            partition_key = partition_key_value(record)
            document = record.model_dump(mode="json") | {
                "id": self._document_id(record),
                "_partition_key": partition_key,
            }
            self._upsert_document(container=container, document=document, partition_key=partition_key)
        # Invalidate only the affected record types' cached scans -- a
        # write to Capability records must not force Relationship/Claim/
        # Entity readers (which didn't change) to pay a fresh full scan on
        # their next call, the same "invalidate precisely, not everything"
        # discipline load_all_embeddings's own per-record-type cache key
        # already follows.
        for record_type in {record.type for record in records}:
            self._records_cache.pop(record_type, None)

    def load_brain_records(
        self, *, scope: str, record_type: RecordType | None = None
    ) -> list[BrainRecordUnion]:
        # Cosmos has no directory-scope concept -- filter by EvidenceUnit.source_id
        # or by a matching id prefix, since `scope` in local mode is a
        # directory name like "incidents/case_228086" derived from a
        # source/case id embedded in most Brain ids the same way.
        types = [record_type] if record_type is not None else list(_MODEL_BY_TYPE)
        records: list[BrainRecordUnion] = []
        for one_type in types:
            for record in self._query_container(self._container_for(one_type), one_type):
                if self._record_matches_scope(record, scope):
                    records.append(record)
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
        for one_type in types:
            for record in self._query_container(self._container_for(one_type), one_type):
                if wanted_ids is not None and record.id not in wanted_ids:
                    continue
                records.append(record)
        return records

    # -- Ingestion runs ------------------------------------------------------

    def save_ingestion_run(self, run: dict[str, Any]) -> None:
        run_id = run.get("run_id")
        if not run_id:
            raise ValueError("save_ingestion_run requires a 'run_id' key")
        self._upsert_document(
            container=self.settings.containers[INGESTION_RUNS_CONTAINER],
            document={**run, "id": str(run_id), "_partition_key": str(run_id)},
            partition_key=str(run_id),
        )

    def load_ingestion_run(self, run_id: str) -> dict[str, Any] | None:
        container = self.settings.containers[INGESTION_RUNS_CONTAINER]
        doc = self._get_document(container=container, document_id=run_id, partition_key=run_id)
        return _strip_cosmos_fields(doc) if doc is not None else None

    def find_scope_for_record(self, record_id: str) -> str | None:
        # Cosmos has no scope concept at all -- save_brain_records() already
        # ignores `scope` entirely (partitions by the record's own
        # content). The only thing that matters here is EXISTENCE: any
        # non-None sentinel signals "this id is already stored, merge into
        # it" to the caller (brain_service/persistence.py's _apply_merge),
        # which then calls save_brain_records(..., scope=<this value>) --
        # a value that gets discarded on arrival either way.
        for record in self.load_brain_context():
            if record.id == record_id:
                return "cosmos"
        return None

    # -- Embeddings ------------------------------------------------------------

    def save_embeddings(self, embeddings: list[dict[str, Any]]) -> None:
        container = self.settings.containers[EMBEDDINGS_CONTAINER]
        for embedding in embeddings:
            record_id = embedding["record_id"]
            document = {
                **embedding,
                "id": record_id,
                "_partition_key": embedding["record_type"],
            }
            self._upsert_document(container=container, document=document, partition_key=embedding["record_type"])
        self._embeddings_cache.clear()

    def load_all_embeddings(self, record_type: RecordType | None = None) -> list[dict[str, Any]]:
        cache_key = record_type.value if record_type is not None else None
        if cache_key in self._embeddings_cache:
            return self._embeddings_cache[cache_key]

        container = self.settings.containers[EMBEDDINGS_CONTAINER]
        query = "SELECT * FROM c"
        parameters: list[dict[str, Any]] = []
        if record_type is not None:
            query = "SELECT * FROM c WHERE c.record_type = @record_type"
            parameters = [{"name": "@record_type", "value": record_type.value}]

        results: list[dict[str, Any]] = []
        continuation: str | None = None
        while True:
            payload, continuation = self._cross_partition_query(
                container=container, query=query, parameters=parameters, continuation=continuation
            )
            results.extend(_strip_cosmos_fields(doc) for doc in payload.get("Documents") or [])
            if not continuation:
                break

        self._embeddings_cache[cache_key] = results
        return results

    # -- internals -----------------------------------------------------------

    def _container_for(self, record_type: RecordType) -> str:
        role_name = CONTAINER_BY_RECORD_TYPE[record_type]
        return self.settings.containers[role_name]

    def _document_id(self, record: BrainRecordUnion) -> str:
        # Cosmos document ids may not contain "/", "\", "?", "#" -- Brain
        # ids use ":" freely (e.g. "entity:system:wcs"), which IS allowed,
        # so no rewriting is needed; this exists as the one place that
        # assumption is asserted rather than silently relied upon.
        forbidden = set("/\\?#")
        if forbidden.intersection(record.id):
            raise AzureCosmosStorageError(
                f"{record.id!r} contains a character forbidden in a Cosmos document id: {forbidden}"
            )
        return record.id

    def _record_matches_scope(self, record: BrainRecordUnion, scope: str) -> bool:
        # scope looks like "incidents/case_228086" or "operational_sources/manual_x" --
        # the trailing path segment is the source/case identifier embedded
        # in most Brain ids (e.g. "evidence:case_228086:event_001",
        # "claim:incident_228086_...:...").
        token = scope.rstrip("/").rsplit("/", 1)[-1]
        token = token.removeprefix("case_")
        return token in record.id if token else True

    def _query_container(self, container: str, record_type: RecordType) -> list[BrainRecordUnion]:
        if record_type in self._records_cache:
            return self._records_cache[record_type]

        model = _MODEL_BY_TYPE[record_type]
        results: list[BrainRecordUnion] = []
        continuation: str | None = None
        while True:
            payload, continuation = self._cross_partition_query(
                container=container,
                query="SELECT * FROM c",
                parameters=[],
                continuation=continuation,
            )
            for row in payload.get("Documents") or []:
                results.append(model.model_validate(_strip_cosmos_fields(row)))
            if not continuation:
                break
        self._records_cache[record_type] = results
        return results

    def _get_document(self, *, container: str, document_id: str, partition_key: str) -> dict[str, Any] | None:
        resource_id = f"dbs/{self.settings.database}/colls/{container}/docs/{document_id}"
        url = f"{self.settings.endpoint.rstrip('/')}/{resource_id}"
        headers = self._auth_headers(verb="GET", resource_type="docs", resource_id=resource_id, partition_key=partition_key)
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=_TIMEOUT_SECONDS) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            details = exc.read().decode("utf-8", errors="replace")
            raise AzureCosmosStorageError(f"Cosmos get failed for {document_id!r}: HTTP {exc.code} {details}") from exc

    def _upsert_document(self, *, container: str, document: dict[str, Any], partition_key: str) -> None:
        collection_id = f"dbs/{self.settings.database}/colls/{container}"
        url = f"{self.settings.endpoint.rstrip('/')}/{collection_id}/docs"
        headers = self._auth_headers(
            verb="POST", resource_type="docs", resource_id=collection_id, partition_key=partition_key
        )
        headers["x-ms-documentdb-is-upsert"] = "true"
        request = urllib.request.Request(
            url, data=json.dumps(document).encode("utf-8"), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=_TIMEOUT_SECONDS):
                return
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise AzureCosmosStorageError(
                f"Cosmos upsert failed for container={container} doc={document.get('id')}: HTTP {exc.code} {details}"
            ) from exc

    def _cross_partition_query(
        self,
        *,
        container: str,
        query: str,
        parameters: list[dict[str, Any]],
        continuation: str | None,
    ) -> tuple[dict[str, Any], str | None]:
        collection_id = f"dbs/{self.settings.database}/colls/{container}"
        url = f"{self.settings.endpoint.rstrip('/')}/{collection_id}/docs"
        request_date = formatdate(timeval=None, localtime=False, usegmt=True)
        headers = {
            "Authorization": self._authorization_header(
                verb="POST", resource_type="docs", resource_id=collection_id, date=request_date
            ),
            "Content-Type": "application/query+json",
            "x-ms-date": request_date,
            "x-ms-version": _API_VERSION,
            "x-ms-documentdb-isquery": "True",
            "x-ms-documentdb-query-enablecrosspartition": "true",
            "x-ms-max-item-count": "100",
        }
        if continuation:
            headers["x-ms-continuation"] = continuation
        body = {"query": query, "parameters": parameters}
        request = urllib.request.Request(
            url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=_TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
                next_continuation = response.headers.get("x-ms-continuation") or None
                return payload, next_continuation
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise AzureCosmosStorageError(
                f"Cosmos query failed for container={container}: HTTP {exc.code} {details}"
            ) from exc

    def _auth_headers(self, *, verb: str, resource_type: str, resource_id: str, partition_key: str) -> dict[str, str]:
        request_date = formatdate(timeval=None, localtime=False, usegmt=True)
        return {
            "Authorization": self._authorization_header(
                verb=verb, resource_type=resource_type, resource_id=resource_id, date=request_date
            ),
            "Content-Type": "application/json",
            "x-ms-date": request_date,
            "x-ms-version": _API_VERSION,
            "x-ms-documentdb-partitionkey": json.dumps([partition_key]),
        }

    def _authorization_header(self, *, verb: str, resource_type: str, resource_id: str, date: str) -> str:
        string_to_sign = f"{verb.lower()}\n{resource_type.lower()}\n{resource_id}\n{date.lower()}\n\n"
        key_bytes = base64.b64decode(self.settings.key)
        signature = base64.b64encode(
            hmac.new(key_bytes, string_to_sign.encode("utf-8"), hashlib.sha256).digest()
        ).decode("utf-8")
        return f"type=master&ver=1.0&sig={urllib.parse.quote(signature, safe='')}"
