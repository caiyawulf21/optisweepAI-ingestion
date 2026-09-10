"""Adapter: finalized runbook output -> ingest_stage_output's generic
`records` shape. Shared by BOTH pipelines' Stage 6
(incidence's create_stage6_incident_runbooks and operational's
finalize_operational_runbooks) since both produce the identical finalized
runbook shape (procedure_id/title/summary/steps/...).

Only copies fields already present on a finalized runbook; no judgment
(capability resolution, Procedure record construction) happens here.
"""

from __future__ import annotations

from typing import Any


def finalized_runbooks_to_records(finalized_runbooks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for runbook in finalized_runbooks:
        step_texts = [
            f"{step.get('title', '')}: {step.get('instruction', '')}"
            for step in runbook.get("steps", [])
            if isinstance(step, dict)
        ]
        text_parts = [
            str(runbook.get("summary") or ""),
            str(runbook.get("when_to_use") or ""),
            *step_texts,
        ]
        records.append(
            {
                "procedure_id": runbook.get("procedure_id"),
                "candidate_id": runbook.get("candidate_id"),
                "title": runbook.get("title"),
                "text": "\n".join(part for part in text_parts if part),
                "procedure_type": runbook.get("procedure_type"),
                "responsible_role": runbook.get("responsible_role"),
                "capability_tags": runbook.get("capability_tags", []),
                "source_refs": runbook.get("source_refs", []),
                "locator_hint": {"section": runbook.get("procedure_id")},
            }
        )
    return records
