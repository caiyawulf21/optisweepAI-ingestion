from __future__ import annotations

import copy
from datetime import UTC, datetime
from typing import Any


def promote_pass_through_runbook(runbook: dict[str, Any]) -> dict[str, Any]:
    promoted = copy.deepcopy(runbook)
    metadata = dict(promoted.get("metadata") or {})
    metadata.update(
        {
            "merge_status": "pass_through",
            "created_by": "stage_7_pass_through",
            "promoted_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        }
    )
    promoted["metadata"] = metadata
    promoted["merged_from_procedure_ids"] = [str(promoted.get("procedure_id") or "")]
    promoted["canonical_source_procedure_ids"] = list(promoted["merged_from_procedure_ids"])
    return promoted
