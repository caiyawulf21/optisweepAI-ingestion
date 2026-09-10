"""Re-run Stage 5/6/8 for Day 1 + Day 2 training videos, then shared 6.5-10."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.paths import OPERATIONAL_ROOT, SHARED_OUTPUT, SHARED_SCRIPTS, discover_source_roots
from orchestration.runners import CommandError

OP_SCRIPTS = OPERATIONAL_ROOT / "scripts"
SOURCES = [
    OPERATIONAL_ROOT / "data" / "output" / "training_video_day1",
    OPERATIONAL_ROOT / "data" / "output" / "training_video_day2",
]


def run_streaming(script: Path, args: list[str]) -> None:
    command = [sys.executable, "-u", str(script), *args]
    print(f"$ {' '.join(command)}", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    env.setdefault("LLM_MIN_INTERVAL_SEC", "4")
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


def regen_source(out: Path) -> None:
    stage1 = out / "stage_1_source_bundle"
    stage2 = out / "stage_2_source_artifacts"
    stage4 = out / "stage_4_operational_context"
    stage5 = out / "stage_5_runbook_candidates"
    stage6 = out / "stage_6_finalized_runbooks"
    segments = stage1 / "training_video_slide_segments.json"
    stage2_artifacts = stage2 / "source_artifacts.json"
    for required in (segments, stage2_artifacts, stage4 / "operational_context.json"):
        if not required.exists():
            raise FileNotFoundError(required)

    print(f"=== Stage 2 prepare: {out.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage2_prepare_training_video_for_extraction.py",
        [
            "--training-segments",
            str(segments),
            "--source-artifacts",
            str(stage2_artifacts),
            "--output-dir",
            str(out),
        ],
    )

    # Stage 6 write-only overwrite leaves dropped candidate IDs behind; clear before regen.
    _clear_dir_files(stage6 / "finalized_runbooks", {".json"})
    _clear_dir_files(stage6 / "review_markdown" / "runbooks", {".md", ".html"})
    _clear_dir_files(out / "stage_8_relationship_linking" / "finalized_runbooks_linked", {".json"})

    print(f"=== Stage 5: {out.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage5_extract_runbook_candidates.py",
        [
            "--source-bundle",
            str(stage2 / "source_bundle.json"),
            "--source-artifacts",
            str(stage2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(stage4 / "operational_context.json"),
            "--output-dir",
            str(out),
            "--llm",
            "--max-workers",
            "1",
        ],
    )

    print(f"=== Stage 6: {out.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage6_finalize_runbooks.py",
        [
            "--runbook-candidates",
            str(stage5 / "runbook_candidates.json"),
            "--source-artifacts",
            str(stage2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(stage4 / "operational_context.json"),
            "--source-bundle",
            str(stage2 / "source_bundle.json"),
            "--output-dir",
            str(out),
            "--max-workers",
            "1",
        ],
    )

    print(f"=== Stage 8 (ops): {out.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage8_link_relationships.py",
        [
            "--output-dir",
            str(out),
            "--source-artifacts",
            str(stage2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(stage4 / "operational_context.json"),
            "--finalized-runbooks-dir",
            str(stage6 / "finalized_runbooks"),
            "--runbook-candidates",
            str(stage5 / "runbook_candidates.json"),
        ],
    )


def run_shared() -> None:
    roots = discover_source_roots()
    shared_out = SHARED_OUTPUT
    shared_out.mkdir(parents=True, exist_ok=True)
    pool_dir = shared_out / "stage_6_5_runbook_pool"
    stage7_dir = shared_out / "stage_7_merged_runbooks"
    stage8_dir = shared_out / "stage_8_finalized_playbooks"
    stage85_dir = shared_out / "stage_8_5_relationship_linking"
    case_ids = [
        root.name.removeprefix("case_")
        for root in roots
        if root.name.startswith("case_")
    ] or ["228086", "228723"]

    print(f"=== Shared 6.5–10 over {len(roots)} roots ===", flush=True)
    for root in roots:
        print(f"  - {root}", flush=True)

    stage65_args = ["--output-dir", str(shared_out)]
    for root in roots:
        stage65_args.extend(["--source-root", str(root)])
    print("=== Shared 6.5 ===", flush=True)
    run_streaming(SHARED_SCRIPTS / "stage6_5_build_runbook_pool.py", stage65_args)

    print("=== Shared 7 ===", flush=True)
    run_streaming(
        SHARED_SCRIPTS / "stage7_merge_runbooks.py",
        ["--pool-dir", str(pool_dir), "--output-dir", str(shared_out), "--llm"],
    )

    stage8_args = [
        "--pool-dir",
        str(pool_dir),
        "--stage7-dir",
        str(stage7_dir),
        "--output-dir",
        str(shared_out),
        "--llm",
    ]
    for case_id in case_ids:
        stage8_args.extend(["--case-id", case_id])
    print("=== Shared 8 ===", flush=True)
    run_streaming(SHARED_SCRIPTS / "stage8_finalize_playbooks.py", stage8_args)

    stage85_args = [
        "--output-dir",
        str(shared_out),
        "--stage7-dir",
        str(stage7_dir),
        "--stage8-dir",
        str(stage8_dir),
    ]
    for root in roots:
        stage85_args.extend(["--source-root", str(root)])
    print("=== Shared 8.5 ===", flush=True)
    run_streaming(SHARED_SCRIPTS / "stage8_5_link_relationships.py", stage85_args)

    stage9_args = [
        "--stage7-dir",
        str(stage7_dir),
        "--stage8-dir",
        str(stage8_dir),
        "--stage85-dir",
        str(stage85_dir),
        "--output-dir",
        str(shared_out),
    ]
    for root in roots:
        stage9_args.extend(["--source-root", str(root)])
    print("=== Shared 9 ===", flush=True)
    run_streaming(SHARED_SCRIPTS / "stage9_validate_corpus.py", stage9_args)

    stage10_args = [
        "--stage7-dir",
        str(stage7_dir),
        "--stage8-dir",
        str(stage8_dir),
        "--output-dir",
        str(shared_out),
    ]
    for root in roots:
        stage10_args.extend(["--source-root", str(root)])
    print("=== Shared 10 ===", flush=True)
    run_streaming(SHARED_SCRIPTS / "stage10_generate_embeddings.py", stage10_args)


def restore_day1_from_head() -> None:
    day1 = SOURCES[0]
    paths = [
        day1 / "stage_5_runbook_candidates",
        day1 / "stage_6_finalized_runbooks",
    ]
    command = ["git", "checkout", "HEAD", "--", *[str(p) for p in paths]]
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=str(REPO_ROOT), check=True)


def main() -> None:
    print("=== Regen Day 1 + Day 2 Stage 5/6/8 with tightened prompts ===", flush=True)
    print(f"LLM_MIN_INTERVAL_SEC={os.environ.get('LLM_MIN_INTERVAL_SEC', '4')} (default 4)", flush=True)
    try:
        for source in SOURCES:
            if not source.exists():
                raise FileNotFoundError(source)
            regen_source(source)
        run_shared()
    except Exception:
        print("=== Regen failed; restoring Day1 stage_5/stage_6 from HEAD ===", flush=True)
        restore_day1_from_head()
        raise
    print("=== Day 1 + Day 2 regen complete (Stage 11 skipped) ===", flush=True)


if __name__ == "__main__":
    main()
