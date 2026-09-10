"""Adapter: relationship link output -> ingest_stage_output's generic
`records` shape. Shared by BOTH pipelines' Stage 8
(incidence's link_incident_relationships and operational's
link_source_relationships) since both produce the identical link shape
(link_id/link_type/source_record_id/target_record_id/...).
"""

from __future__ import annotations

from typing import Any


def relationship_links_to_records(relationship_links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for link in relationship_links:
        text = (
            f"{link.get('source_record_type')} {link.get('source_record_id')} "
            f"is linked to {link.get('target_record_type')} {link.get('target_record_id')} "
            f"via {link.get('link_type')} (method: {link.get('link_method')}, "
            f"confidence: {link.get('confidence')})."
        )
        records.append(
            {
                "link_id": link.get("link_id"),
                "link_type": link.get("link_type"),
                "text": text,
                "source_record_type": link.get("source_record_type"),
                "source_record_id": link.get("source_record_id"),
                "target_record_type": link.get("target_record_type"),
                "target_record_id": link.get("target_record_id"),
                "confidence": link.get("confidence"),
                "needs_sme_review": link.get("needs_sme_review"),
                "source_refs": [],
                "locator_hint": {"section": link.get("link_id")},
            }
        )
    return records
