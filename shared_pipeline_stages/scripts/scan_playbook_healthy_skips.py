from __future__ import annotations

import json
from pathlib import Path

from shared_pipeline_stages.stage_8.normalize import (
    _is_recovery_node,
    _node_requires_recovery_prerequisite,
)

REPO = Path(__file__).resolve().parents[2]


def main() -> None:
    paths = [p for p in REPO.rglob("canonical_playbooks.json") if "node_modules" not in str(p)]
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        playbooks = data.get("playbooks") if isinstance(data, dict) else data
        if not isinstance(playbooks, list):
            continue
        for playbook in playbooks:
            nodes = {
                str(node.get("node_id") or ""): node
                for node in playbook.get("nodes") or []
                if isinstance(node, dict)
            }
            issues: list[str] = []
            for node in nodes.values():
                node_id = str(node.get("node_id") or "")
                for branch in node.get("branches") or []:
                    if not isinstance(branch, dict):
                        continue
                    next_id = str(branch.get("next_node_id") or "")
                    branch_id = str(branch.get("branch_id") or "")
                    if "inferred_healthy" in branch_id and next_id:
                        target = nodes.get(next_id)
                        if (
                            target
                            and _node_requires_recovery_prerequisite(target)
                            and not _is_recovery_node(node)
                        ):
                            issues.append(f"{node_id} {branch_id} -> {next_id} skips recovery")
                    if branch.get("outcome") == "healthy" and next_id == node_id:
                        issues.append(f"{node_id} healthy self-loop")
            if issues:
                print(f"{path.relative_to(REPO)} :: {playbook.get('playbook_id')}")
                for issue in issues:
                    print(f"  {issue}")


if __name__ == "__main__":
    main()
