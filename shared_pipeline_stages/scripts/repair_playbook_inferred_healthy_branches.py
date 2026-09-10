from __future__ import annotations

import json
from pathlib import Path

from shared_pipeline_stages.stage_8.normalize import build_branches_from_hints

REPO_ROOT = Path(__file__).resolve().parents[2]
PATHS = [
    path
    for path in REPO_ROOT.rglob("canonical_playbooks.json")
    if "node_modules" not in str(path)
]


def repair_playbook(playbook: dict) -> None:
    nodes = [node for node in playbook.get("nodes") or [] if isinstance(node, dict)]
    hints = [hint for hint in playbook.get("branch_hints") or [] if isinstance(hint, dict)]
    playbook["branch_hints"] = hints
    for node in nodes:
        node["branches"] = build_branches_from_hints(node, hints, all_nodes=nodes)
        by_outcome: dict[str, str] = {}
        for branch in node.get("branches") or []:
            if not isinstance(branch, dict):
                continue
            outcome = str(branch.get("outcome") or "")
            if outcome and outcome not in by_outcome:
                by_outcome[outcome] = str(branch.get("next_node_id") or "")
        for outcome in node.get("decision_outcomes") or []:
            if not isinstance(outcome, dict):
                continue
            label = str(outcome.get("outcome_label") or "")
            if label in by_outcome:
                outcome["next_node_id"] = by_outcome[label]
    playbook_branches = []
    for node in nodes:
        if str(node.get("node_type") or "") != "branching_condition":
            continue
        for branch in node.get("branches") or []:
            if isinstance(branch, dict):
                playbook_branches.append({**branch, "from_node_id": node.get("node_id")})
    if "branches" in playbook:
        playbook["branches"] = playbook_branches


def main() -> None:
    for path in PATHS:
        data = json.loads(path.read_text(encoding="utf-8"))
        playbooks = data.get("playbooks") if isinstance(data, dict) else data
        if not isinstance(playbooks, list):
            print(f"SKIP unexpected shape {path}")
            continue
        for playbook in playbooks:
            if not isinstance(playbook, dict):
                continue
            repair_playbook(playbook)
            print(f"OK {path.relative_to(REPO_ROOT)} :: {playbook.get('playbook_id')}")
        if isinstance(data, dict):
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            path.write_text(json.dumps(playbooks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"WROTE {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
