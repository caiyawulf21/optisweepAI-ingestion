"""Run Day 2 training video through source Stages 1-8 + shared 6.5-10 (no Stage 11)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.paths import (
    OPERATIONAL_ROOT,
    TRAINING_STAGE1_SCRIPT,
    TRAINING_STAGE2_SCRIPT,
)
from orchestration.runners import CommandError

VIDEO_DIR = OPERATIONAL_ROOT / "data" / "input" / "videos"
VIDEO = VIDEO_DIR / (
    "FORTNA OptiSweep Training - Day 2 [NOTE Morning Location is Different]"
    "-20260318_082628-Meeting Recording.mp4"
)
VTT = VIDEO_DIR / (
    "FORTNA OptiSweep Training - Day 2 [NOTE Morning Location is Different]"
    "-20260318_082628-Meeting Recording-en-US.vtt"
)
OUTPUT_DIR = OPERATIONAL_ROOT / "data" / "output" / "training_video_day2"
SOURCE_ID = "training_video_day2"
SOURCE_TITLE = "FORTNA OptiSweep Training Day 2"
CROP_BOX = "0,68,1676,1012"
OP_SCRIPTS = OPERATIONAL_ROOT / "scripts"


def run_streaming(script: Path, args: list[str]) -> None:
    command = [sys.executable, str(script), *args]
    print(f"$ {' '.join(command)}", flush=True)
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="", flush=True)
    code = process.wait()
    if code != 0:
        raise CommandError(command, code, "", f"exit {code}")


def main() -> None:
    if not VIDEO.exists():
        raise FileNotFoundError(VIDEO)
    if not VTT.exists():
        raise FileNotFoundError(VTT)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stage1 = OUTPUT_DIR / "stage_1_source_bundle"
    stage2 = OUTPUT_DIR / "stage_2_source_artifacts"
    stage4 = OUTPUT_DIR / "stage_4_operational_context"
    stage5 = OUTPUT_DIR / "stage_5_runbook_candidates"
    stage6 = OUTPUT_DIR / "stage_6_finalized_runbooks"

    print("=== Day 2 ingest (through Stage 10, skip 11) ===", flush=True)
    print(f"video: {VIDEO}", flush=True)
    print(f"vtt:   {VTT}", flush=True)
    print(f"out:   {OUTPUT_DIR}", flush=True)

    print("=== Stage 1: training video bundle (crop=day1, ocr=none) ===", flush=True)
    run_streaming(
        TRAINING_STAGE1_SCRIPT,
        [
            "--source-video",
            str(VIDEO),
            "--transcript-vtt",
            str(VTT),
            "--output-dir",
            str(OUTPUT_DIR),
            "--source-id",
            SOURCE_ID,
            "--source-title",
            SOURCE_TITLE,
            "--crop-box",
            CROP_BOX,
            "--ocr-backend",
            "none",
            "--max-segment-seconds",
            "120",
        ],
    )

    print("=== Stage 2: prepare training video for extraction ===", flush=True)
    run_streaming(
        TRAINING_STAGE2_SCRIPT,
        [
            "--training-segments",
            str(stage1 / "training_video_slide_segments.json"),
            "--source-artifacts",
            str(stage1 / "source_artifacts.json"),
            "--output-dir",
            str(OUTPUT_DIR),
        ],
    )

    print("=== Stage 4: operational context ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage4_extract_operational_context.py",
        [
            "--source-bundle",
            str(stage2 / "source_bundle.json"),
            "--source-artifacts",
            str(stage2 / "source_artifacts_enriched.json"),
            "--output-dir",
            str(OUTPUT_DIR),
            "--llm",
        ],
    )

    print("=== Stage 5: runbook candidates ===", flush=True)
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
            str(OUTPUT_DIR),
            "--llm",
            "--max-workers",
            "4",
        ],
    )

    print("=== Stage 6: finalize runbooks ===", flush=True)
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
            str(OUTPUT_DIR),
            "--max-workers",
            "4",
        ],
    )

    print("=== Stage 8: relationship linking ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage8_link_relationships.py",
        [
            "--output-dir",
            str(OUTPUT_DIR),
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

    print("=== Shared Stages 6.5,7,8,8.5,9,10 (no Stage 11) ===", flush=True)
    from orchestration.paths import SHARED_OUTPUT, SHARED_SCRIPTS, discover_source_roots

    roots = discover_source_roots()
    if not any(root.name == SOURCE_ID for root in roots):
        raise RuntimeError(f"{SOURCE_ID} missing from discover_source_roots(): {roots}")
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

    print(f"shared source roots ({len(roots)}):", flush=True)
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

    print("=== Day 2 ingest complete (Stage 11 skipped) ===", flush=True)


if __name__ == "__main__":
    main()
