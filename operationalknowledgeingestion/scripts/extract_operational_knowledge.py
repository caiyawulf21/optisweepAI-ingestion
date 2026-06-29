"""Stages 1-6 CLI: run operational source extraction into stage folders.

This script mirrors the incident extraction orchestrator: it coordinates the
implemented local operational stages and writes each stage into a stage-scoped
folder under the requested output directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optisweep_ingestion.stage_paths import STAGE_DIR_NAMES, normalize_stage, stage_dir
from optisweep_ingestion.tools.artifact_enricher import AzureOpenAIArtifactClient, enrich_source_artifacts
from optisweep_ingestion.tools.artifact_extractor import extract_source_artifacts
from optisweep_ingestion.tools.candidate_pool_builder import build_candidate_pool
from optisweep_ingestion.tools.operational_context_extractor import AzureOpenAIContextClient, extract_operational_context
from optisweep_ingestion.tools.runbook_candidate_extractor import AzureOpenAIRunbookCandidateClient, extract_runbook_candidates
from optisweep_ingestion.tools.source_bundle_builder import build_source_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract operational knowledge from a source PDF.")
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stages", default="1,2", help="Comma-separated stages to run. Supports 1,2,3,4,5,6.")
    parser.add_argument("--llm", action="store_true", help="Use Azure OpenAI for LLM-backed stages 3, 4, and 5.")
    parser.add_argument("--max-workers", type=int, default=4, help="Concurrent LLM calls for stages that support it.")
    parser.add_argument("--backfill-missing-sections", action="store_true", help="Stage 5: add conservative candidates for missed procedural sections.")
    parser.add_argument("--source-bundle-id", default=None)
    parser.add_argument("--source-document-id", default=None)
    parser.add_argument("--source-id", default=None)
    parser.add_argument("--source-type", default="manual")
    parser.add_argument("--source-title", default=None)
    parser.add_argument("--source-version", default=None)
    parser.add_argument("--ingestion-batch-id", default=None)
    args = parser.parse_args()

    stages = {_normalize_supported_stage(stage) for stage in args.stages.split(",") if stage.strip()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stage1_dir = stage_dir(args.output_dir, "1")
    stage2_dir = stage_dir(args.output_dir, "2")
    stage3_dir = stage_dir(args.output_dir, "3")
    stage4_dir = stage_dir(args.output_dir, "4")
    stage5_dir = stage_dir(args.output_dir, "5")
    stage6_dir = stage_dir(args.output_dir, "6")

    if "1" in stages:
        bundle = build_source_bundle(
            source_pdf=args.source_pdf,
            output_dir=stage1_dir,
            source_bundle_id=args.source_bundle_id,
            source_document_id=args.source_document_id,
            source_id=args.source_id,
            source_type=args.source_type,
            source_title=args.source_title,
            source_version=args.source_version,
            ingestion_batch_id=args.ingestion_batch_id,
        )
        print(f"Stage 1 source bundle written: {stage1_dir / 'source_bundle.json'}")
        print(f"Stage 1 pages: {len(bundle.pages)}")
        print(f"Stage 1 sections: {len(bundle.sections)}")

    if "2" in stages:
        source_bundle_path = _require_existing(
            "Stage 2 requires Stage 1 source_bundle.json. Run stage 1 first.",
            stage1_dir / "source_bundle.json",
            args.output_dir / "source_bundle.json",
        )
        artifacts, report = extract_source_artifacts(source_bundle_path, args.source_pdf, stage2_dir)
        print(f"Stage 2 source artifacts written: {stage2_dir / 'source_artifacts.json'}")
        print(f"Stage 2 artifact report written: {stage2_dir / 'artifact_extraction_report.json'}")
        print(f"Stage 2 artifacts created: {len(artifacts)}")
        print(f"Stage 2 images saved: {report['total_images_saved']}")

    if "3" in stages:
        if not args.llm:
            raise ValueError("Stage 3 requires --llm. Fake artifact enrichment is not supported.")
        source_artifacts_path = _require_existing(
            "Stage 3 requires Stage 2 source_artifacts.json. Run stage 2 first.",
            stage2_dir / "source_artifacts.json",
            args.output_dir / "source_artifacts.json",
        )
        artifact_report_path = _require_existing(
            "Stage 3 requires Stage 2 artifact_extraction_report.json. Run stage 2 first.",
            stage2_dir / "artifact_extraction_report.json",
            args.output_dir / "artifact_extraction_report.json",
        )
        client = AzureOpenAIArtifactClient()
        artifacts, report = enrich_source_artifacts(
            source_artifacts_path,
            artifact_report_path,
            stage3_dir,
            client,
            llm_used=True,
            max_workers=args.max_workers,
        )
        print(f"Stage 3 enriched artifacts written: {stage3_dir / 'source_artifacts_enriched.json'}")
        print(f"Stage 3 enrichment report written: {stage3_dir / 'artifact_enrichment_report.json'}")
        print(f"Stage 3 enriched artifacts: {report['enriched_artifact_count']} of {len(artifacts)}")
        print(f"Stage 3 failed artifacts: {report['failed_artifact_count']}")

    if "4" in stages:
        if not args.llm:
            raise ValueError("Stage 4 requires --llm. Fake context generation is not supported.")
        source_bundle_path = _require_existing(
            "Stage 4 requires Stage 1 source_bundle.json. Run stage 1 first.",
            stage1_dir / "source_bundle.json",
            args.output_dir / "source_bundle.json",
        )
        source_artifacts_path = _require_existing(
            "Stage 4 requires Stage 3 source_artifacts_enriched.json. Run stage 3 first.",
            stage3_dir / "source_artifacts_enriched.json",
            args.output_dir / "source_artifacts_enriched.json",
        )
        client = AzureOpenAIContextClient()
        contexts, report = extract_operational_context(
            source_bundle_path=source_bundle_path,
            source_artifacts_path=source_artifacts_path,
            output_dir=stage4_dir,
            llm_client=client,
            llm_used=True,
        )
        print(f"Stage 4 operational context written: {stage4_dir / 'operational_context.json'}")
        print(f"Stage 4 extraction report written: {stage4_dir / 'operational_context_extraction_report.json'}")
        print(f"Stage 4 context records extracted: {len(contexts)}")
        print(f"Stage 4 failed packets: {len(report['failed_packets'])}")

    if "5" in stages:
        if not args.llm:
            raise ValueError("Stage 5 requires --llm. Fake runbook candidate generation is not supported.")
        source_bundle_path = _require_existing(
            "Stage 5 requires Stage 1 source_bundle.json. Run stage 1 first.",
            stage1_dir / "source_bundle.json",
            args.output_dir / "source_bundle.json",
        )
        source_artifacts_path = _require_existing(
            "Stage 5 requires Stage 3 source_artifacts_enriched.json. Run stage 3 first.",
            stage3_dir / "source_artifacts_enriched.json",
            args.output_dir / "source_artifacts_enriched.json",
        )
        operational_context_path = _require_existing(
            "Stage 5 requires Stage 4 operational_context.json. Run stage 4 first.",
            stage4_dir / "operational_context.json",
            args.output_dir / "operational_context.json",
        )
        client = AzureOpenAIRunbookCandidateClient()
        candidates, report = extract_runbook_candidates(
            source_bundle_path=source_bundle_path,
            source_artifacts_path=source_artifacts_path,
            operational_context_path=operational_context_path,
            output_dir=stage5_dir,
            llm_client=client,
            llm_used=True,
            max_workers=args.max_workers,
            backfill_missing_sections=args.backfill_missing_sections,
        )
        print(f"Stage 5 runbook candidates written: {stage5_dir / 'runbook_candidates.json'}")
        print(f"Stage 5 extraction report written: {stage5_dir / 'runbook_candidate_extraction_report.json'}")
        print(f"Stage 5 coverage report written: {stage5_dir / 'runbook_candidate_coverage_report.json'}")
        print(f"Stage 5 candidates extracted: {len(candidates)}")
        print(f"Stage 5 failed packets: {len(report['failed_packets'])}")

    if "6" in stages:
        candidates_path = _require_existing(
            "Stage 6 requires Stage 5 runbook_candidates.json. Run stage 5 first.",
            stage5_dir / "runbook_candidates.json",
            args.output_dir / "runbook_candidates.json",
        )
        pool = build_candidate_pool(candidate_paths=[candidates_path], output_dir=stage6_dir)
        print(f"Stage 6 candidate pool written: {stage6_dir / 'candidate_pool.json'}")
        print(f"Stage 6 candidate clusters generated: {pool.candidate_cluster_count}")


def _normalize_supported_stage(value: str) -> str:
    stage = normalize_stage(value)
    if stage not in {"1", "2", "3", "4", "5", "6"}:
        raise ValueError("Implemented operational extraction stages are 1,2,3,4,5,6.")
    return stage


def _require_existing(message: str, *paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(message + " Missing: " + ", ".join(str(path) for path in paths))


if __name__ == "__main__":
    main()
