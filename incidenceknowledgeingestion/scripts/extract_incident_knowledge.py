"""Stages 1-3 CLI: run local incident source loading, OCR, packets, and enrichment.

This script orchestrates implemented incidence stages, copies the raw PDF when
requested, and writes stage-scoped output folders for a case output directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optisweep_incidence_ingestion.stage1_source_package import build_incident_source_package
from optisweep_incidence_ingestion.stage2_5_artifact_enrichment_packets import build_artifact_enrichment_packets
from optisweep_incidence_ingestion.stage2_ocr_artifacts import extract_incident_ocr_artifacts
from optisweep_incidence_ingestion.stage3_artifact_enrichment import (
    AzureOpenAIIncidentArtifactClient,
    enrich_incident_artifacts,
)


STAGE_DIR_NAMES = {
    "1": "stage_1_source_package",
    "2": "stage_2_ocr_artifacts",
    "2.5": "stage_2_5_artifact_enrichment_packets",
    "3": "stage_3_artifact_enrichment",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract incident evidence from a PDF.")
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--source-title", default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stages", default="1,2", help="Comma-separated stages to run. Supports 1,2,2.5,3.")
    parser.add_argument("--llm", action="store_true", help="Use Azure OpenAI for Stage 3 artifact enrichment.")
    parser.add_argument("--max-workers", type=int, default=4, help="Concurrent Stage 3 LLM calls.")
    parser.add_argument("--stage3-prompt-path", type=Path, default=None)
    parser.add_argument("--stage3-no-images", action="store_true", help="Do not send artifact images to the Stage 3 LLM.")
    parser.add_argument("--ocr-backend", default="tesseract", choices=["none", "tesseract"])
    parser.add_argument("--tesseract-command", default=None)
    parser.add_argument("--render-zoom", type=float, default=3.0)
    parser.add_argument(
        "--include-detected-crops",
        action="store_true",
        help="Also emit OpenCV detected-region crops. Default keeps actual embedded images only, with crops as fallback.",
    )
    parser.add_argument("--copy-source", action="store_true", help="Copy source PDF into output raw_source folder.")
    args = parser.parse_args()

    stages = {_normalize_stage(stage) for stage in args.stages.split(",") if stage.strip()}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stage1_dir = _stage_dir(args.output_dir, "1")
    stage2_dir = _stage_dir(args.output_dir, "2")
    stage2_5_dir = _stage_dir(args.output_dir, "2.5")
    stage3_dir = _stage_dir(args.output_dir, "3")
    source_pdf = args.source_pdf
    if args.copy_source:
        raw_dir = stage1_dir / "raw_source"
        raw_dir.mkdir(parents=True, exist_ok=True)
        copied = raw_dir / source_pdf.name
        if source_pdf.resolve() != copied.resolve():
            shutil.copy2(source_pdf, copied)

    stage1_package_path = stage1_dir / "incident_source_package.json"
    stage2_package_path = stage2_dir / "incident_source_package.json"
    if "1" in stages:
        package = build_incident_source_package(
            source_pdf=source_pdf,
            output_dir=stage1_dir,
            case_id=args.case_id,
            source_title=args.source_title,
        )
        print(f"Stage 1 source package written: {stage1_package_path}")
        print(f"Stage 1 page count: {package['page_count']}")
    if "2" in stages:
        package_path = _first_existing(stage1_package_path, args.output_dir / "incident_source_package.json")
        if not package_path:
            raise FileNotFoundError(f"Stage 2 requires {stage1_package_path}. Run stage 1 first.")
        artifacts, report = extract_incident_ocr_artifacts(
            source_package_path=package_path,
            source_pdf=source_pdf,
            output_dir=stage2_dir,
            ocr_backend=args.ocr_backend,
            tesseract_command=args.tesseract_command,
            render_zoom=args.render_zoom,
            include_detected_crops=args.include_detected_crops,
        )
        print(f"Stage 2 source artifacts written: {stage2_dir / 'source_artifacts.json'}")
        print(f"Stage 2 artifact extraction report written: {stage2_dir / 'artifact_extraction_report.json'}")
        print(f"Stage 2 artifacts created: {len(artifacts)}")
        print(f"Stage 2 duplicate groups: {report['duplicate_group_count']}")
    if "2.5" in stages:
        package_path = _first_existing(stage2_package_path, args.output_dir / "incident_source_package.json")
        page_inventory_path = _first_existing(stage2_dir / "page_inventory.json", args.output_dir / "page_inventory.json")
        artifacts_path = _first_existing(stage2_dir / "source_artifacts.json", args.output_dir / "source_artifacts.json")
        report_path = _first_existing(stage2_dir / "artifact_extraction_report.json", args.output_dir / "artifact_extraction_report.json")
        missing = [
            str(path)
            for path in [stage2_package_path, stage2_dir / "page_inventory.json", stage2_dir / "source_artifacts.json"]
            if not path.exists()
        ]
        if not package_path or not page_inventory_path or not artifacts_path:
            raise FileNotFoundError(
                "Stage 2.5 requires Stage 2 outputs. Missing staged files: " + ", ".join(missing)
            )
        packets, report = build_artifact_enrichment_packets(
            source_package_path=package_path,
            page_inventory_path=page_inventory_path,
            source_artifacts_path=artifacts_path,
            artifact_extraction_report_path=report_path,
            output_dir=stage2_5_dir,
        )
        print(f"Stage 2.5 enrichment packets written: {stage2_5_dir / 'artifact_enrichment_packets.json'}")
        print(f"Stage 2.5 packet report written: {stage2_5_dir / 'artifact_enrichment_packet_report.json'}")
        print(f"Stage 2.5 packets created: {len(packets)}")
        print(f"Stage 2.5 context roles: {report['context_roles']}")
    if "3" in stages:
        if not args.llm:
            raise ValueError("Stage 3 requires --llm. Fake artifact enrichment is not supported.")
        packets_path = _first_existing(
            stage2_5_dir / "artifact_enrichment_packets.json",
            args.output_dir / "stage_2_5_artifact_enrichment" / "artifact_enrichment_packets.json",
        )
        package_path = _first_existing(stage2_5_dir / "incident_source_package.json", stage2_package_path)
        if not packets_path:
            raise FileNotFoundError(f"Stage 3 requires {stage2_5_dir / 'artifact_enrichment_packets.json'}. Run stage 2.5 first.")
        client = AzureOpenAIIncidentArtifactClient(
            prompt_path=args.stage3_prompt_path,
            include_images=not args.stage3_no_images,
        )
        enriched_artifacts, report = enrich_incident_artifacts(
            artifact_enrichment_packets_path=packets_path,
            source_package_path=package_path,
            output_dir=stage3_dir,
            llm_client=client,
            llm_used=True,
            max_workers=args.max_workers,
        )
        print(f"Stage 3 enriched artifacts written: {stage3_dir / 'source_artifacts_enriched.json'}")
        print(f"Stage 3 artifact enrichment report written: {stage3_dir / 'artifact_enrichment_report.json'}")
        print(f"Stage 3 enriched artifacts: {report['enriched_artifact_count']} of {len(enriched_artifacts)}")
        print(f"Stage 3 failed artifacts: {report['failed_artifact_count']}")
        if report["failed_artifact_count"] == len(enriched_artifacts):
            raise RuntimeError("Stage 3 failed for every artifact. See artifact_enrichment_report.json for details.")


def _stage_dir(output_dir: Path, stage: str) -> Path:
    return output_dir / STAGE_DIR_NAMES[stage]


def _normalize_stage(value: str) -> str:
    stage = value.strip().lower().replace("stage_", "").replace("stage", "")
    if stage in {"25", "2_5", "2-5"}:
        return "2.5"
    if stage in STAGE_DIR_NAMES:
        return stage
    raise ValueError(f"Unsupported stage '{value}'. Supported stages: 1,2,2.5")


def _first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


if __name__ == "__main__":
    main()
