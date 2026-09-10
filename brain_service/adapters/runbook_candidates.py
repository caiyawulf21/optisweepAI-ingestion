"""Adapter: runbook candidate output -> ingest_stage_output's generic
`records` shape. Shared by BOTH pipelines' Stage 5
(incidence's create_stage5_incident_candidates and operational's
extract_runbook_candidates) since both produce the identical candidate
shape (candidate_id/title/candidate_goal/summary/rough_steps/...).

Only copies fields already present on a runbook candidate; no judgment
(no capability resolution, no procedure synthesis) happens here -- that
stays inside classify_candidate/reconcile_candidate.
"""

from __future__ import annotations

from typing import Any


def runbook_candidates_to_records(runbook_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for candidate in runbook_candidates:
        text_parts = [
            candidate.get("candidate_goal") or "",
            candidate.get("summary") or "",
            *[str(step) for step in candidate.get("rough_steps", [])],
        ]
        records.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "title": candidate.get("title"),
                "text": "\n".join(part for part in text_parts if part),
                "likely_procedure_type": candidate.get("likely_procedure_type"),
                "likely_role_required": candidate.get("likely_role_required"),
                "source_refs": candidate.get("source_refs", []),
                "locator_hint": {"section": candidate.get("candidate_id")},
            }
        )
    return records
