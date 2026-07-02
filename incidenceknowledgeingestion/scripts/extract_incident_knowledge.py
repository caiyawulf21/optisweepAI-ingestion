"""Incident ingestion CLI: run local incident extraction stages.

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
from optisweep_incidence_ingestion.stage2_ocr_artifacts import QwenArtifactGate, extract_incident_ocr_artifacts
from optisweep_incidence_ingestion.stage3_artifact_enrichment import (
    AzureOpenAIIncidentArtifactClient,
    enrich_incident_artifacts,
)
from optisweep_incidence_ingestion.stage4_canonical_incident_record import (
    AzureOpenAIStage4Client,
    create_stage4_canonical_incident_record_and_timeline,
)
from optisweep_incidence_ingestion.stage5_runbook_candidates import (
    AzureOpenAIStage5PlaybookCandidateClient,
    AzureOpenAIStage5RunbookCandidateClient,
    create_stage5_incident_candidates,
)
from optisweep_incidence_ingestion.stage6_runbook_finalization import (
    AzureOpenAIStage6RunbookFinalizationClient,
    create_stage6_incident_runbooks,
)


STAGE_DIR_NAMES = {
    "1": "stage_1_source_package",
    "2": "stage_2_ocr_artifacts",
    "2.5": "stage_2_5_artifact_enrichment_packets",
    "3": "stage_3_artifact_enrichment",
    "4": "stage_4_canonical_incident_record",
    "5": "stage_5_runbook_candidates",
    "6": "stage_6_finalized_runbooks",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract incident evidence from a PDF.")
    parser.add_argument("--source-pdf", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--source-title", default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--stages", default="1,2", help="Comma-separated stages to run. Supports 1,2,2.5,3,4,5,6.")
    parser.add_argument("--llm", action="store_true", help="Use Azure OpenAI for LLM-backed stages.")
    parser.add_argument("--max-workers", type=int, default=4, help="Concurrent Stage 3 LLM calls.")
    parser.add_argument("--stage3-prompt-path", type=Path, default=None)
    parser.add_argument("--stage3-no-images", action="store_true", help="Do not send artifact images to the Stage 3 LLM.")
    parser.add_argument("--stage4-canonical-prompt-path", type=Path, default=None)
    parser.add_argument("--stage4-timeline-prompt-path", type=Path, default=None)
    parser.add_argument("--stage4-page-chunk-chars", type=int, default=7000)
    parser.add_argument("--stage4-artifact-chunk-size", type=int, default=8)
    parser.add_argument("--stage4-review-evidence-path", type=Path, default=None)
    parser.add_argument("--stage5-prompt-path", type=Path, default=None, help="Stage 5 runbook candidate prompt path.")
    parser.add_argument(
        "--stage5-playbook-prompt-path",
        type=Path,
        default=None,
        help="Deprecated alias for --stage5-playbook-prompt-a-path.",
    )
    parser.add_argument("--stage5-playbook-prompt-a-path", type=Path, default=None)
    parser.add_argument("--stage5-playbook-prompt-b-path", type=Path, default=None)
    parser.add_argument("--stage6-prompt-path", type=Path, default=None, help="Stage 6 runbook finalization prompt path.")
    parser.add_argument("--ocr-backend", default="tesseract", choices=["none", "tesseract"])
    parser.add_argument("--tesseract-command", default=None)
    parser.add_argument("--stage2-artifact-gate", default="qwen", choices=["none", "qwen"])
    parser.add_argument("--stage2-qwen-model", default="Qwen/Qwen2.5-VL-3B-Instruct")
    parser.add_argument("--stage2-qwen-device", default=None)
    parser.add_argument("--stage2-qwen-max-new-tokens", type=int, default=180)
    parser.add_argument("--stage2-qwen-local-files-only", action="store_true", default=True)
    parser.add_argument("--stage2-qwen-allow-download", dest="stage2_qwen_local_files_only", action="store_false")
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
    stage4_dir = _stage_dir(args.output_dir, "4")
    stage5_dir = _stage_dir(args.output_dir, "5")
    stage6_dir = _stage_dir(args.output_dir, "6")
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
        artifact_gate = None
        if args.stage2_artifact_gate == "qwen":
            qwen_model = _resolve_qwen_model_path(args.stage2_qwen_model, args.stage2_qwen_local_files_only)
            artifact_gate = QwenArtifactGate(
                model_name=qwen_model,
                device=args.stage2_qwen_device,
                max_new_tokens=args.stage2_qwen_max_new_tokens,
                local_files_only=args.stage2_qwen_local_files_only,
            )
        artifacts, report = extract_incident_ocr_artifacts(
            source_package_path=package_path,
            source_pdf=source_pdf,
            output_dir=stage2_dir,
            ocr_backend=args.ocr_backend,
            tesseract_command=args.tesseract_command,
            render_zoom=args.render_zoom,
            include_detected_crops=args.include_detected_crops,
            artifact_gate=artifact_gate,
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
    if "4" in stages:
        if not args.llm:
            raise ValueError("Stage 4 requires --llm. Fake canonical incident/timeline extraction is not supported.")
        package_path = _first_existing(stage3_dir / "incident_source_package.json", stage2_5_dir / "incident_source_package.json")
        page_inventory_path = _first_existing(stage2_dir / "page_inventory.json", args.output_dir / "page_inventory.json")
        enriched_artifacts_path = _first_existing(
            stage3_dir / "source_artifacts_enriched.json",
            args.output_dir / "stage_3_artifact_enrichment" / "source_artifacts_enriched.json",
        )
        artifact_enrichment_report_path = _first_existing(
            stage3_dir / "artifact_enrichment_report.json",
            args.output_dir / "stage_3_artifact_enrichment" / "artifact_enrichment_report.json",
        )
        review_evidence_path = args.stage4_review_evidence_path or _first_existing(stage4_dir / "stage4_review_evidence.json")
        missing = [
            str(path)
            for path in [
                stage3_dir / "incident_source_package.json",
                stage2_dir / "page_inventory.json",
                stage3_dir / "source_artifacts_enriched.json",
                stage3_dir / "artifact_enrichment_report.json",
            ]
            if not path.exists()
        ]
        if not package_path or not page_inventory_path or not enriched_artifacts_path or not artifact_enrichment_report_path:
            raise FileNotFoundError(
                "Stage 4 requires Stage 2 page inventory and Stage 3 enriched artifacts. Missing staged files: "
                + ", ".join(missing)
            )
        client = AzureOpenAIStage4Client(
            canonical_prompt_path=args.stage4_canonical_prompt_path,
            timeline_prompt_path=args.stage4_timeline_prompt_path,
        )
        canonical_record, canonical_report, timeline_events, timeline_report = create_stage4_canonical_incident_record_and_timeline(
            source_package_path=package_path,
            page_inventory_path=page_inventory_path,
            source_artifacts_enriched_path=enriched_artifacts_path,
            artifact_enrichment_report_path=artifact_enrichment_report_path,
            output_dir=stage4_dir,
            llm_client=client,
            page_chunk_target_chars=args.stage4_page_chunk_chars,
            artifact_chunk_size=args.stage4_artifact_chunk_size,
            review_evidence_path=review_evidence_path,
        )
        print(f"Stage 4 canonical incident record written: {stage4_dir / 'canonical_incident_record.json'}")
        print(f"Stage 4 timeline events written: {stage4_dir / 'timeline_events.json'}")
        print(f"Stage 4 timeline event count: {len(timeline_events.get('events') or [])}")
        if canonical_report.get("validation_errors") or timeline_report.get("validation_errors"):
            raise RuntimeError("Stage 4 completed with validation errors. See Stage 4 extraction reports.")
    if "5" in stages:
        if not args.llm:
            raise ValueError("Stage 5 requires --llm. Fake incident runbook/playbook candidate discovery is not supported.")
        package_path = _first_existing(stage4_dir / "incident_source_package.json", stage3_dir / "incident_source_package.json")
        canonical_record_path = _first_existing(stage4_dir / "canonical_incident_record.json")
        timeline_events_path = _first_existing(stage4_dir / "timeline_events.json")
        stage4_evidence_chunks_path = _first_existing(stage4_dir / "stage4_evidence_chunks.json")
        enriched_artifacts_path = _first_existing(stage3_dir / "source_artifacts_enriched.json")
        missing = [
            str(path)
            for path in [
                stage4_dir / "incident_source_package.json",
                stage4_dir / "canonical_incident_record.json",
                stage4_dir / "timeline_events.json",
                stage4_dir / "stage4_evidence_chunks.json",
                stage3_dir / "source_artifacts_enriched.json",
            ]
            if not path.exists()
        ]
        if (
            not package_path
            or not canonical_record_path
            or not timeline_events_path
            or not stage4_evidence_chunks_path
            or not enriched_artifacts_path
        ):
            raise FileNotFoundError(
                "Stage 5 requires Stage 3 enriched artifacts and Stage 4 incident/timeline outputs. Missing staged files: "
                + ", ".join(missing)
            )
        runbook_client = AzureOpenAIStage5RunbookCandidateClient(prompt_path=args.stage5_prompt_path)
        prompt_dir = SRC / "optisweep_incidence_ingestion" / "prompts"
        prompt_a_path = (
            args.stage5_playbook_prompt_a_path
            or args.stage5_playbook_prompt_path
            or prompt_dir / "stage5_playbook_candidate_discovery_prompt_a_one_per_incident.md"
        )
        prompt_b_path = (
            args.stage5_playbook_prompt_b_path
            or prompt_dir / "stage5_playbook_candidate_discovery_prompt_b_multi_flow.md"
        )
        playbook_clients = {
            "playbook_prompt_a_one_per_incident": AzureOpenAIStage5PlaybookCandidateClient(prompt_path=prompt_a_path),
            "playbook_prompt_b_multi_flow": AzureOpenAIStage5PlaybookCandidateClient(prompt_path=prompt_b_path),
        }
        candidates, report, playbook_results = create_stage5_incident_candidates(
            source_package_path=package_path,
            canonical_incident_record_path=canonical_record_path,
            timeline_events_path=timeline_events_path,
            stage4_evidence_chunks_path=stage4_evidence_chunks_path,
            source_artifacts_enriched_path=enriched_artifacts_path,
            output_dir=stage5_dir,
            runbook_llm_client=runbook_client,
            playbook_llm_clients=playbook_clients,
        )
        print(f"Stage 5 runbook candidates written: {stage5_dir / 'runbook_candidates.json'}")
        print(f"Stage 5 extraction report written: {stage5_dir / 'runbook_candidate_extraction_report.json'}")
        print(f"Stage 5 candidate count: {len(candidates)}")
        for mode_slug, (playbook_candidates, playbook_report) in playbook_results.items():
            mode_dir = stage5_dir / mode_slug
            print(f"Stage 5 {mode_slug} playbook candidates written: {mode_dir / 'playbook_candidates.json'}")
            print(f"Stage 5 {mode_slug} extraction report written: {mode_dir / 'playbook_candidate_extraction_report.json'}")
            print(f"Stage 5 {mode_slug} candidate count: {len(playbook_candidates)}")
        if report.get("validation_errors") or any(
            playbook_report.get("validation_errors") for _candidates, playbook_report in playbook_results.values()
        ):
            raise RuntimeError("Stage 5 completed with validation errors. See Stage 5 extraction reports.")
    if "6" in stages:
        if not args.llm:
            raise ValueError("Stage 6 requires --llm. Fake incident runbook finalization is not supported.")
        candidates_path = _first_existing(stage5_dir / "runbook_candidates.json")
        package_path = _first_existing(stage5_dir / "incident_source_package.json", stage4_dir / "incident_source_package.json")
        canonical_record_path = _first_existing(stage4_dir / "canonical_incident_record.json")
        timeline_events_path = _first_existing(stage4_dir / "timeline_events.json")
        stage4_evidence_chunks_path = _first_existing(stage4_dir / "stage4_evidence_chunks.json")
        enriched_artifacts_path = _first_existing(stage3_dir / "source_artifacts_enriched.json")
        missing = [
            str(path)
            for path in [
                stage5_dir / "runbook_candidates.json",
                stage4_dir / "canonical_incident_record.json",
                stage4_dir / "timeline_events.json",
                stage4_dir / "stage4_evidence_chunks.json",
                stage3_dir / "source_artifacts_enriched.json",
            ]
            if not path.exists()
        ]
        if (
            not candidates_path
            or not package_path
            or not canonical_record_path
            or not timeline_events_path
            or not stage4_evidence_chunks_path
            or not enriched_artifacts_path
        ):
            raise FileNotFoundError(
                "Stage 6 requires Stage 3 enriched artifacts, Stage 4 outputs, and Stage 5 runbook candidates. Missing staged files: "
                + ", ".join(missing)
            )
        client = AzureOpenAIStage6RunbookFinalizationClient(prompt_path=args.stage6_prompt_path)
        finalized, report = create_stage6_incident_runbooks(
            runbook_candidates_path=candidates_path,
            source_artifacts_enriched_path=enriched_artifacts_path,
            canonical_incident_record_path=canonical_record_path,
            timeline_events_path=timeline_events_path,
            stage4_evidence_chunks_path=stage4_evidence_chunks_path,
            source_package_path=package_path,
            output_dir=stage6_dir,
            llm_client=client,
            max_workers=args.max_workers,
        )
        print(f"Stage 6 finalized runbooks written: {stage6_dir / 'finalized_runbooks'}")
        print(f"Stage 6 review markdown written: {stage6_dir / 'review_markdown' / 'runbooks'}")
        print(f"Stage 6 finalization report written: {stage6_dir / 'runbook_finalization_report.json'}")
        print(f"Stage 6 finalized runbook count: {len(finalized)}")
        print(f"Stage 6 failed candidates: {report.get('failed_candidate_count', 0)}")


def _stage_dir(output_dir: Path, stage: str) -> Path:
    return output_dir / STAGE_DIR_NAMES[stage]


def _normalize_stage(value: str) -> str:
    stage = value.strip().lower().replace("stage_", "").replace("stage", "")
    if stage in {"25", "2_5", "2-5"}:
        return "2.5"
    if stage in STAGE_DIR_NAMES:
        return stage
    raise ValueError(f"Unsupported stage '{value}'. Supported stages: 1,2,2.5,3,4,5,6")


def _first_existing(*paths: Path) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def _resolve_qwen_model_path(model_name: str, local_files_only: bool) -> str:
    if not local_files_only or Path(model_name).exists() or "/" not in model_name:
        return model_name
    cache_root = Path.home() / ".cache" / "huggingface" / "hub"
    model_cache_name = "models--" + model_name.replace("/", "--")
    snapshots_dir = cache_root / model_cache_name / "snapshots"
    if not snapshots_dir.exists():
        return model_name
    snapshots = sorted(
        [path for path in snapshots_dir.iterdir() if path.is_dir()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return str(snapshots[0]) if snapshots else model_name


if __name__ == "__main__":
    main()
