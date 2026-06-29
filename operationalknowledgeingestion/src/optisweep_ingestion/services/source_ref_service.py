"""Source reference and lineage helpers for source knowledge extraction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from operationalknowledgeingestion.src.optisweep_ingestion.schemas.source_lineage import ALLOWED_SOURCE_TYPES, SourceLineage


def make_ingestion_batch_id(timestamp: datetime | None = None) -> str:
    moment = timestamp or datetime.now(timezone.utc)
    return moment.strftime("batch_%Y%m%dT%H%M%SZ")


def lineage_from_bundle(bundle: dict[str, Any] | Any) -> SourceLineage:
    if hasattr(bundle, "model_dump"):
        data = bundle.model_dump(mode="json")
    else:
        data = bundle
    metadata = data.get("source_metadata") or {}
    source_document = data.get("source_document") or {}
    source_type = metadata.get("source_type") or source_document.get("source_type") or "manual"
    if source_type not in ALLOWED_SOURCE_TYPES:
        source_type = "manual"
    return SourceLineage(
        source_id=str(metadata.get("source_id") or data.get("source_bundle_id") or ""),
        source_type=source_type,
        source_title=str(
            metadata.get("source_title")
            or source_document.get("title")
            or data.get("source_bundle_id")
            or ""
        ),
        source_version=metadata.get("source_version") or source_document.get("version"),
        ingestion_batch_id=str(metadata.get("ingestion_batch_id") or make_ingestion_batch_id()),
        source_document_id=str(
            metadata.get("source_document_id") or source_document.get("source_document_id") or ""
        ),
    )


def lineage_to_dict(lineage: SourceLineage) -> dict[str, Any]:
    payload = lineage.model_dump(mode="json")
    return {key: value for key, value in payload.items() if key != "source_document_id"}


def apply_lineage(record: dict[str, Any], lineage: SourceLineage) -> dict[str, Any]:
    updated = dict(record)
    for field, value in lineage_to_dict(lineage).items():
        if value not in (None, ""):
            updated[field] = value
    updated.setdefault("source_refs", [])
    return updated


def build_source_ref(
    lineage: SourceLineage,
    *,
    page: int | None = None,
    page_start: int | None = None,
    page_end: int | None = None,
    section_id: str | None = None,
    figure_id: str | None = None,
    figure_number: str | None = None,
    table_id: str | None = None,
    quote_or_summary: str | None = None,
) -> dict[str, Any]:
    ref: dict[str, Any] = {
        "source_id": lineage.source_id,
        "source_type": lineage.source_type,
        "source_title": lineage.source_title,
        "source_version": lineage.source_version,
        "ingestion_batch_id": lineage.ingestion_batch_id,
        "source_document_id": lineage.source_document_id,
    }
    if page is not None:
        ref["page"] = page
    if page_start is not None:
        ref["page_start"] = page_start
    if page_end is not None:
        ref["page_end"] = page_end
    if section_id:
        ref["section_id"] = section_id
    if figure_id:
        ref["figure_id"] = figure_id
    if figure_number:
        ref["figure_number"] = figure_number
    if table_id:
        ref["table_id"] = table_id
    if quote_or_summary:
        ref["quote_or_summary"] = quote_or_summary
    return ref


def record_has_lineage(record: dict[str, Any]) -> bool:
    return all(str(record.get(field) or "").strip() for field in ("source_id", "source_type", "ingestion_batch_id"))


def record_has_source_refs(record: dict[str, Any]) -> bool:
    refs = record.get("source_refs")
    return isinstance(refs, list) and len(refs) > 0
