from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_6_5.json_utils import read_json, write_json
from shared_pipeline_stages.stage_8.linked_runbook_surface import attach_linked_runbooks
from shared_pipeline_stages.stage_8.normalize import (
    attach_catalog_gaps,
    enrich_node_structure,
    sanitize_playbook_branch_graph,
)

VARIANTS = {
    "prompt_a_one_per_incident": "prompt_a_one_per_incident",
    "prompt_b_multi_flow": "prompt_b_multi_flow",
    "prompt_a": "prompt_a",
    "prompt_b": "prompt_b",
}


def migrate_stage8_artifacts(stage8_dir: Path, runbooks_path: Path) -> int:
    runbook_payload = read_json(runbooks_path)
    runbooks = runbook_payload.get("runbooks") if isinstance(runbook_payload, dict) else runbook_payload
    runbooks_by_id = {
        str(runbook.get("procedure_id") or ""): runbook
        for runbook in runbooks or []
        if isinstance(runbook, dict) and str(runbook.get("procedure_id") or "").strip()
    }
    migrated = 0
    for variant in VARIANTS.values():
        canonical_path = stage8_dir / variant / "canonical_playbooks.json"
        if not canonical_path.is_file():
            continue
        payload = read_json(canonical_path)
        for playbook in payload.get("playbooks") or []:
            if not isinstance(playbook, dict):
                continue
            for node in playbook.get("nodes") or []:
                if not isinstance(node, dict):
                    continue
                old_references = list(node.get("linked_runbooks") or [])
                old_ids = [
                    str(item.get("procedure_id") or "")
                    for item in old_references
                    if isinstance(item, dict) and str(item.get("procedure_id") or "").strip()
                ]
                if old_ids and not node.get("resolved_runbook_ids"):
                    node["resolved_runbook_ids"] = old_ids
                node.update(
                    enrich_node_structure(
                        node,
                        decision_outcomes=list(node.get("decision_outcomes") or []),
                        branches=list(node.get("branches") or []),
                    )
                )
                attach_linked_runbooks(node, runbooks_by_id=runbooks_by_id)
                if old_references and not node["linked_runbooks"]:
                    node["linked_runbooks"] = [
                        {
                            key: item.get(key)
                            for key in (
                                "procedure_id",
                                "title",
                                "procedure_type",
                                "purpose",
                                "role_required",
                                "audience_roles",
                            )
                            if item.get(key) is not None
                        }
                        for item in old_references
                        if isinstance(item, dict) and item.get("procedure_id")
                    ]
                    node["evidence_collection_procedures"] = [
                        dict(item) for item in node["linked_runbooks"]
                    ]
                attach_catalog_gaps(node)
            sanitize_playbook_branch_graph(playbook)
            migrated += 1
        write_json(canonical_path, payload)
    return migrated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage8_dir", type=Path)
    parser.add_argument("runbooks_path", type=Path)
    args = parser.parse_args()
    print(f"Migrated {migrate_stage8_artifacts(args.stage8_dir, args.runbooks_path)} playbooks.")


if __name__ == "__main__":
    main()
