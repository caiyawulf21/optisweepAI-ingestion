"""Rerun pilot incident Stage 5/6/8 then shared 6.5/7/8 (playbook linking)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.paths import INCIDENT_SCRIPT, SHARED_OUTPUT, SHARED_SCRIPTS, discover_source_roots
from orchestration.runners import CommandError

INCIDENTS = REPO_ROOT / "incidenceknowledgeingestion" / "data" / "output" / "incidents"
CASES = [
    {
        "case_id": "228086",
        "pdf": REPO_ROOT
        / "incidenceknowledgeingestion"
        / "data"
        / "input"
        / "incidents"
        / "Case 228086 Data.pdf",
        "title": "Case 228086 - UPS Haslet OptiSweep Incident Evidence",
    },
    {
        "case_id": "228723",
        "pdf": REPO_ROOT
        / "incidenceknowledgeingestion"
        / "data"
        / "input"
        / "incidents"
        / "Case 228723 Data.pdf",
        "title": "Case 228723",
    },
    {
        "case_id": "218550",
        "pdf": INCIDENTS / "case_218550" / "stage_1_source_package" / "raw_source" / "Case 218550 Data.pdf",
        "title": "Case 218550",
    },
    {
        "case_id": "223554",
        "pdf": INCIDENTS / "case_223554" / "stage_1_source_package" / "raw_source" / "Case 223554 Data.pdf",
        "title": "Case 223554",
    },
]


def run_streaming(script: Path, args: list[str]) -> None:
    command = [sys.executable, "-u", str(script), *args]
    print(f"$ {' '.join(command)}", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    env.setdefault("LLM_MIN_INTERVAL_SEC", "20")
    env.setdefault("LLM_429_MAX_ATTEMPTS", "24")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(REPO_ROOT),
        env=env,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
    code = process.wait()
    if code != 0:
        raise CommandError(command, code, "", f"exit {code}")


def _clear_dir_files(directory: Path, suffixes: set[str]) -> None:
    if not directory.exists():
        return
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in suffixes:
            path.unlink()


def rerun_case(case: dict[str, object]) -> None:
    case_id = str(case["case_id"])
    pdf = Path(case["pdf"])
    out = INCIDENTS / f"case_{case_id}"
    if not pdf.exists():
        raise FileNotFoundError(pdf)
    stage5 = out / "stage_5_runbook_candidates"
    stage6 = out / "stage_6_finalized_runbooks"
    print(f"=== Incident Stage 5/6/8: case_{case_id} ===", flush=True)
    run_streaming(
        INCIDENT_SCRIPT,
        [
            "--source-pdf",
            str(pdf),
            "--case-id",
            case_id,
            "--source-title",
            str(case["title"]),
            "--output-dir",
            str(out),
            "--stages",
            "5,6,8",
            "--llm",
        ],
    )
    candidates_path = stage5 / "runbook_candidates.json"
    count = 0
    if candidates_path.exists():
        data = json.loads(candidates_path.read_text(encoding="utf-8"))
        count = len(data) if isinstance(data, list) else 0
    finalized = list((stage6 / "finalized_runbooks").glob("*.json")) if (stage6 / "finalized_runbooks").exists() else []
    print(
        f"case_{case_id}: stage5_runbook_candidates={count} stage6_finalized={len(finalized)}",
        flush=True,
    )
    if case_id == "228086" and count == 0:
        print(
            "WARN case_228086: Stage 5 returned 0 runbook candidates "
            "(prior Stage 6 may be restored for pool continuity)",
            flush=True,
        )


def run_shared() -> None:
    from orchestration.runners.shared_publish import run_shared_publish_pipeline

    roots = discover_source_roots()
    case_ids = [str(c["case_id"]) for c in CASES]
    print(f"=== Shared 6.5/7/8 (pool always rebuilt) over {len(roots)} roots ===", flush=True)
    for root in roots:
        print(f"  - {root}", flush=True)
    run_shared_publish_pipeline(
        source_roots=roots,
        stages="6.5,7,8",
        use_llm=True,
        case_ids=case_ids,
    )
    pool_path = SHARED_OUTPUT / "stage_6_5_runbook_pool" / "runbook_pool.json"
    if pool_path.exists():
        pool = json.loads(pool_path.read_text(encoding="utf-8"))
        rows = pool if isinstance(pool, list) else pool.get("runbooks") or []
        hit_228086 = [
            r
            for r in rows
            if "228086" in json.dumps(r.get("source_lineage") or r.get("source_refs") or r, ensure_ascii=True)
            or "228086" in str(r.get("procedure_id") or "")
            or "228086" in str(r.get("candidate_id") or "")
        ]
        print(f"Pool runbooks: {len(rows)}; with 228086 lineage/id: {len(hit_228086)}", flush=True)


def main() -> None:
    import argparse
    import time

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        default=",".join(c["case_id"] for c in CASES),
        help="Comma-separated case ids (default: all pilots, 228086 first).",
    )
    parser.add_argument("--skip-shared", action="store_true")
    parser.add_argument("--cooldown-sec", type=int, default=180, help="Sleep before first LLM call.")
    parser.add_argument("--between-case-sec", type=int, default=90)
    args = parser.parse_args()
    wanted = {c.strip() for c in args.cases.split(",") if c.strip()}
    selected = [c for c in CASES if c["case_id"] in wanted]
    if not selected:
        raise SystemExit(f"No matching cases in {wanted}")

    os.chdir(REPO_ROOT)
    if args.cooldown_sec > 0:
        print(f"Cooldown {args.cooldown_sec}s for Azure rate limit...", flush=True)
        time.sleep(args.cooldown_sec)

    for idx, case in enumerate(selected):
        if idx > 0 and args.between_case_sec > 0:
            print(f"Inter-case pause {args.between_case_sec}s...", flush=True)
            time.sleep(args.between_case_sec)
        case_id = str(case["case_id"])
        out = INCIDENTS / f"case_{case_id}"
        stage6 = out / "stage_6_finalized_runbooks"
        finalized_dir = stage6 / "finalized_runbooks"
        backup_dir = stage6 / "_pre_rerun_backup_finalized"
        if finalized_dir.exists() and any(finalized_dir.glob("*.json")):
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(finalized_dir, backup_dir)
        _clear_dir_files(finalized_dir, {".json"})
        _clear_dir_files(stage6 / "review_markdown" / "runbooks", {".md", ".html"})
        _clear_dir_files(out / "stage_8_relationship_linking" / "finalized_runbooks_linked", {".json"})
        rerun_case(case)
        finalized = list(finalized_dir.glob("*.json")) if finalized_dir.exists() else []
        if not finalized and backup_dir.exists():
            print(f"case_{case_id}: restoring prior Stage 6 finalized after empty regen", flush=True)
            finalized_dir.mkdir(parents=True, exist_ok=True)
            for path in backup_dir.glob("*.json"):
                shutil.copy2(path, finalized_dir / path.name)

    if not args.skip_shared:
        run_shared()
    print("=== Done ===", flush=True)


if __name__ == "__main__":
    main()
