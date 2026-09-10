"""Light-backfill expects_* on Stage 5 playbook candidates (C-regen without full LLM re-extract).

Best-effort only when fields are empty. Prefer LLM Stage 5 with ontology RAG.
Do not force dual surfaces or rewrite existing expects_* (avoids irrelevant Stage 8 links).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
INCIDENTS = REPO / "incidenceknowledgeingestion" / "data" / "output" / "incidents"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
INCIDENCE_SRC = REPO / "incidenceknowledgeingestion" / "src"
if str(INCIDENCE_SRC) not in sys.path:
    sys.path.insert(0, str(INCIDENCE_SRC))

from shared_pipeline_stages.runbook_tags import _infer_capabilities, _infer_surfaces
from shared_pipeline_stages.taxonomy import canonicalize_surface_id, taxonomy_id_sets

EXPECTS_NODE_TYPES = {"diagnostic_decision", "branching_condition", "validation_gate"}


def _text_blob(node: dict[str, Any]) -> str:
    return " ".join(
        [
            str(node.get("title") or ""),
            str(node.get("intent") or ""),
            str(node.get("goal") or ""),
            str(node.get("runbook_placeholder") or ""),
            str(node.get("needed_runbook_capability") or ""),
            str(node.get("source_supported_description") or ""),
            str(node.get("expected_or_observed_result") or ""),
        ]
    ).lower()


def _infer_audience(text: str, surfaces: list[str], allowed_roles: list[str]) -> list[str]:
    ids = taxonomy_id_sets()["audience_roles"]
    from_node = [r for r in allowed_roles if r in ids]
    if from_node:
        return from_node[:3]
    surf = set(surfaces)
    deep = surf & {"wcs_sql", "wcs_api", "event_viewer", "ignition_gateway", "apidog"}
    if deep:
        if "wcs_sql" in surf or re.search(r"\b(ssms|wcs\s*db|helix)\b", text, re.I):
            out = ["L2_support", "L3_support"]
        else:
            out = ["L2_support"]
        if "rms_ui" in surf:
            out = ["operator", "L1_support", *out]
        return list(dict.fromkeys(out))[:4]
    if "rms_ui" in surf or re.search(r"\b(rms|fleet status)\b", text, re.I):
        return ["operator", "L1_support"]
    if surf & {"physical_floor", "aveva_hmi", "tipper_hmi", "hospital_hmi"}:
        return ["operator", "L1_support"]
    return ["operator", "L1_support"]


def backfill_node(node: dict[str, Any], *, force: bool = False) -> bool:
    node_type = str(node.get("node_type") or "")
    if node_type not in EXPECTS_NODE_TYPES:
        return False
    changed = False
    text = _text_blob(node)
    caps = list(node.get("expects_capability") or [])
    surfaces = list(node.get("expects_surface") or [])
    audience = list(node.get("preferred_audience") or [])

    if force or not caps:
        inferred = _infer_capabilities(text)
        if inferred:
            node["expects_capability"] = inferred[:4]
            changed = True

    if force or not surfaces:
        inferred_s = [canonicalize_surface_id(s) for s in _infer_surfaces(text)]
        inferred_s = list(dict.fromkeys(s for s in inferred_s if s))[:4]
        if inferred_s:
            node["expects_surface"] = inferred_s
            changed = True

    if force or not audience:
        preferred = _infer_audience(
            text,
            list(node.get("expects_surface") or surfaces),
            [str(r) for r in (node.get("allowed_roles") or [])],
        )
        if preferred:
            node["preferred_audience"] = preferred[:4]
            changed = True
    return changed


def _iter_playbooks(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [p for p in data if isinstance(p, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("playbooks"), list):
            return [p for p in data["playbooks"] if isinstance(p, dict)]
        if isinstance(data.get("nodes"), list):
            return [data]
    return []


def process_playbook_file(path: Path, *, force: bool = False) -> dict[str, int]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    playbooks = _iter_playbooks(data)
    if not playbooks:
        return {"files": 0, "nodes_touched": 0, "nodes_changed": 0}

    touched = 0
    changed = 0
    for playbook in playbooks:
        for node in playbook.get("nodes") or []:
            if not isinstance(node, dict):
                continue
            if str(node.get("node_type") or "") not in EXPECTS_NODE_TYPES:
                continue
            touched += 1
            if backfill_node(node, force=force):
                changed += 1

    if changed:
        if isinstance(data, dict) and isinstance(data.get("playbooks"), list):
            data["playbooks"] = playbooks
        elif isinstance(data, list):
            data = playbooks
        path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return {"files": 1, "nodes_touched": touched, "nodes_changed": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incidents-root", type=Path, default=INCIDENTS)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    totals = {"files": 0, "nodes_touched": 0, "nodes_changed": 0}
    paths = sorted(args.incidents_root.glob("case_*/stage_5_runbook_candidates/**/playbook_candidates.json"))
    for path in paths:
        stats = process_playbook_file(path, force=args.force)
        for key, value in stats.items():
            totals[key] += value
        print(f"{path.relative_to(REPO)}: touched={stats['nodes_touched']} changed={stats['nodes_changed']}")
    print(
        f"Done. files={totals['files']} nodes_touched={totals['nodes_touched']} "
        f"nodes_changed={totals['nodes_changed']}"
    )


if __name__ == "__main__":
    main()
