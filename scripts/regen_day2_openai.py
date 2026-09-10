"""Re-run Stage 2 prepare, 5, 6, 8 for Day 2 only (OpenAI deployment via env)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv

from orchestration.paths import OPERATIONAL_ROOT
from scripts.shared_after_source_regen import refresh_shared_after_source_regen
from scripts.regen_day1_day2_stage5_6 import _clear_dir_files, run_streaming

load_dotenv()

OP_SCRIPTS = OPERATIONAL_ROOT / "scripts"
OUT = OPERATIONAL_ROOT / "data" / "output" / "training_video_day2"
STAGE1 = OUT / "stage_1_source_bundle"
STAGE2 = OUT / "stage_2_source_artifacts"
STAGE4 = OUT / "stage_4_operational_context"
STAGE5 = OUT / "stage_5_runbook_candidates"
STAGE6 = OUT / "stage_6_finalized_runbooks"
MAX_WORKERS = os.getenv("REGEN_MAX_WORKERS", "4")
REFRESH_SHARED = os.getenv("REGEN_REFRESH_SHARED", "1").strip().lower() not in {
    "0",
    "false",
    "no",
    "off",
}


def main() -> None:
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    print("=== Day 2 regen (OpenAI) ===", flush=True)
    print(f"AZURE_OPENAI_ENDPOINT={endpoint}", flush=True)
    print(f"AZURE_OPENAI_DEPLOYMENT={deployment}", flush=True)
    print(f"LLM_MIN_INTERVAL_SEC={os.getenv('LLM_MIN_INTERVAL_SEC', '1')}", flush=True)
    print(f"REGEN_MAX_WORKERS={MAX_WORKERS}", flush=True)
    print(f"REGEN_REFRESH_SHARED={REFRESH_SHARED}", flush=True)

    segments = STAGE1 / "training_video_slide_segments.json"
    stage2_artifacts = STAGE2 / "source_artifacts.json"
    for required in (segments, stage2_artifacts, STAGE4 / "operational_context.json"):
        if not required.exists():
            raise FileNotFoundError(required)

    print(f"=== Stage 2 prepare: {OUT.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage2_prepare_training_video_for_extraction.py",
        [
            "--training-segments",
            str(segments),
            "--source-artifacts",
            str(stage2_artifacts),
            "--output-dir",
            str(OUT),
        ],
    )

    print(f"=== Stage 4 artifact re-link: {OUT.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage4_rerun_artifact_link_enrichment.py",
        [
            "--output-dir",
            str(OUT),
            "--source-artifacts",
            str(STAGE2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(STAGE4 / "operational_context.json"),
            "--runbook-candidates",
            str(STAGE5 / "runbook_candidates.json"),
        ],
    )

    _clear_dir_files(STAGE6 / "finalized_runbooks", {".json"})
    _clear_dir_files(STAGE6 / "review_markdown" / "runbooks", {".md", ".html"})
    _clear_dir_files(OUT / "stage_8_relationship_linking" / "finalized_runbooks_linked", {".json"})

    print(f"=== Stage 5: {OUT.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage5_extract_runbook_candidates.py",
        [
            "--source-bundle",
            str(STAGE2 / "source_bundle.json"),
            "--source-artifacts",
            str(STAGE2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(STAGE4 / "operational_context.json"),
            "--output-dir",
            str(OUT),
            "--llm",
            "--max-workers",
            MAX_WORKERS,
        ],
    )

    print(f"=== Stage 6: {OUT.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage6_finalize_runbooks.py",
        [
            "--runbook-candidates",
            str(STAGE5 / "runbook_candidates.json"),
            "--source-artifacts",
            str(STAGE2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(STAGE4 / "operational_context.json"),
            "--source-bundle",
            str(STAGE2 / "source_bundle.json"),
            "--output-dir",
            str(OUT),
            "--max-workers",
            MAX_WORKERS,
        ],
    )

    print(f"=== Stage 8 (ops): {OUT.name} ===", flush=True)
    run_streaming(
        OP_SCRIPTS / "stage8_link_relationships.py",
        [
            "--output-dir",
            str(OUT),
            "--source-artifacts",
            str(STAGE2 / "source_artifacts_enriched.json"),
            "--operational-context",
            str(STAGE4 / "operational_context.json"),
            "--finalized-runbooks-dir",
            str(STAGE6 / "finalized_runbooks"),
            "--runbook-candidates",
            str(STAGE5 / "runbook_candidates.json"),
        ],
    )
    refresh_shared_after_source_regen(label="Day 2")
    print("=== Day 2 OpenAI regen complete ===", flush=True)


if __name__ == "__main__":
    main()
