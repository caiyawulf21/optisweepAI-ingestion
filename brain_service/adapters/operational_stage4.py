"""Adapter: operational Stage 4 (extract_operational_context) context
record output -> ingest_stage_output's generic `records` shape.

Only copies fields already present on a context record; no judgment
happens here.
"""

from __future__ import annotations

from typing import Any


def operational_context_records_to_records(contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for context in contexts:
        text_parts = [str(context.get("summary") or ""), str(context.get("details") or "")]
        records.append(
            {
                "context_id": context.get("context_id"),
                "title": context.get("title"),
                "text": "\n".join(part for part in text_parts if part),
                "context_type": context.get("context_type"),
                "source_refs": context.get("source_refs", []),
                "locator_hint": {"section": context.get("context_id")},
            }
        )
    return records
