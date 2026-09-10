"""Backfill Azure Computer Vision OCR onto existing training-video Stage 1 frame artifacts.

Runs OCR on captured slide images only (no video re-segmentation). Updates
Stage 1 artifacts + segments, then re-runs Stage 2 preparation so
source_artifacts_enriched.json picks up the refreshed ocr_text.

Does not re-run Stage 4+ LLM stages.

Requires AZURE_COMPUTER_VISION_ENDPOINT / AZURE_COMPUTER_VISION_KEY (see
.env.example). Paced for the Azure free tier (20 calls/min) by default via
AZURE_COMPUTER_VISION_MIN_INTERVAL_SEC; override if you're on a higher tier.

By default this only re-OCRs artifacts that are empty or look Tesseract-derived
(so you can compare Azure CV against the existing Tesseract backfill without
double-billing already-strong rows). Pass --force to re-OCR everything.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OP_ROOT = REPO_ROOT / "operationalknowledgeingestion"
OP_SRC = OP_ROOT / "src"
if str(OP_SRC) not in sys.path:
    sys.path.insert(0, str(OP_SRC))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from optisweep_ingestion.stage1_training_video_builder import (  # noqa: E402
    AzureComputerVisionOCRClient,
    detect_title_from_ocr,
    format_timecode,
    ocr_text_hash,
)
from optisweep_ingestion.stage2_training_video_preparer import (  # noqa: E402
    prepare_training_video_for_extraction,
)
from optisweep_ingestion.stage_paths import stage_dir  # noqa: E402
from optisweep_ingestion.utils.json_utils import read_json, write_json  # noqa: E402


def _apply_ocr_fields(
    record: dict,
    *,
    text: str,
    confidence: float | None,
    provenance: dict,
    detected_title: str | None,
) -> None:
    record["ocr_text"] = text
    record["ocr_confidence"] = confidence
    record["ocr_provenance"] = provenance
    record["ocr_text_hash"] = ocr_text_hash(text)
    if detected_title:
        record["detected_title"] = detected_title
        if not record.get("title") or str(record.get("title", "")).startswith("Training Video Segment"):
            record["title"] = detected_title
    metadata = record.get("extraction_metadata")
    if isinstance(metadata, dict):
        metadata["ocr_enabled"] = bool(text or provenance)


def _should_reocr(artifact: dict, *, force: bool) -> bool:
    if force:
        return True
    existing_text = str(artifact.get("ocr_text") or "").strip()
    if not existing_text:
        return True
    existing_backend = str((artifact.get("ocr_provenance") or {}).get("backend") or "").strip().lower()
    # Re-OCR rows that were only ever seen by Tesseract; leave already-Azure-CV
    # rows alone unless --force is passed.
    return existing_backend != "azure_cv"


def backfill_source_root(
    source_root: Path,
    *,
    force: bool,
    run_stage2: bool,
) -> dict:
    stage1 = source_root / "stage_1_source_bundle"
    artifacts_path = stage1 / "source_artifacts.json"
    segments_path = stage1 / "training_video_slide_segments.json"
    report_path = stage1 / "training_video_ingestion_report.json"
    if not artifacts_path.exists() or not segments_path.exists():
        raise FileNotFoundError(f"Missing Stage 1 outputs under {stage1}")

    artifacts = read_json(artifacts_path)
    segments = read_json(segments_path)
    if not isinstance(artifacts, list) or not isinstance(segments, list):
        raise ValueError("Stage 1 artifacts/segments must be JSON lists.")

    client = AzureComputerVisionOCRClient()
    print(f"Azure Computer Vision endpoint: {client.endpoint}", flush=True)

    updated_artifacts = 0
    skipped_artifacts = 0
    failed: list[str] = []
    artifact_by_id = {str(item.get("artifact_id")): item for item in artifacts}
    reocr_candidates = [a for a in artifacts if _should_reocr(a, force=force)]
    print(f"Re-OCR candidates: {len(reocr_candidates)} of {len(artifacts)} artifacts", flush=True)

    for index, artifact in enumerate(artifacts, start=1):
        artifact_id = str(artifact.get("artifact_id") or f"artifact_{index}")
        if not _should_reocr(artifact, force=force):
            skipped_artifacts += 1
            continue
        image_path = Path(str(artifact.get("storage_path") or ""))
        if not image_path.is_file():
            failed.append(f"{artifact_id}: missing image {image_path}")
            continue
        try:
            result = client.extract(image_path)
        except Exception as exc:  # noqa: BLE001
            failed.append(f"{artifact_id}: {exc}")
            continue
        timestamp_seconds = artifact.get("timestamp_seconds")
        provenance = dict(result.provenance or {})
        provenance["backend"] = result.backend
        provenance["source_image_path"] = str(image_path)
        provenance["confidence"] = result.confidence
        if timestamp_seconds is not None:
            provenance["timestamp_seconds"] = timestamp_seconds
            provenance["timestamp_timecode"] = artifact.get("timestamp_timecode") or format_timecode(
                float(timestamp_seconds)
            )
        detected_title = detect_title_from_ocr(result.text) if result.text else None
        _apply_ocr_fields(
            artifact,
            text=result.text,
            confidence=result.confidence,
            provenance=provenance,
            detected_title=detected_title,
        )
        updated_artifacts += 1
        status = "ok" if result.text else "empty"
        print(
            f"[{index}/{len(artifacts)}] {artifact_id}: {status} "
            f"chars={len(result.text)} conf={result.confidence}",
            flush=True,
        )

    updated_segments = 0
    for segment in segments:
        representative_id = str(segment.get("representative_artifact_id") or "")
        artifact = artifact_by_id.get(representative_id)
        if artifact is None:
            artifact_ids = segment.get("artifact_ids") or []
            for candidate_id in artifact_ids:
                artifact = artifact_by_id.get(str(candidate_id))
                if artifact is not None:
                    break
        if artifact is None:
            continue
        ocr_backend = str((artifact.get("ocr_provenance") or {}).get("backend") or "")
        if ocr_backend != "azure_cv" and not force:
            continue
        ocr_text = str(artifact.get("ocr_text") or "")
        segment["ocr_text"] = ocr_text
        segment["ocr_confidence"] = artifact.get("ocr_confidence")
        segment["ocr_provenance"] = artifact.get("ocr_provenance")
        segment["ocr_text_hash"] = artifact.get("ocr_text_hash")
        if artifact.get("detected_title"):
            segment["detected_title"] = artifact.get("detected_title")
        transcript_text = str(segment.get("transcript_text") or "").strip()
        segment["combined_text"] = "\n".join(
            part for part in [transcript_text, ocr_text] if part
        ).strip()
        updated_segments += 1

    write_json(artifacts_path, artifacts)
    write_json(segments_path, segments)

    if report_path.exists():
        report = read_json(report_path)
        if isinstance(report, dict):
            report["ocr_status"] = {
                "enabled": True,
                "backend": "azure_cv",
                "message": f"OCR backend: azure_cv (backfilled via {Path(__file__).name})",
                "endpoint": client.endpoint,
            }
            write_json(report_path, report)

    stage2_summary = None
    if run_stage2:
        stage2_dir = stage_dir(source_root, "2")
        _, prepared, _prep_report = prepare_training_video_for_extraction(
            training_segments_path=segments_path,
            source_artifacts_path=artifacts_path,
            output_dir=stage2_dir,
        )
        stage2_summary = {
            "output_dir": str(stage2_dir),
            "prepared_artifact_count": len(prepared),
            "artifacts_with_ocr": sum(
                1 for item in prepared if str(item.get("ocr_text") or "").strip()
            ),
        }

    with_ocr = sum(1 for item in artifacts if str(item.get("ocr_text") or "").strip())
    summary = {
        "source_root": str(source_root),
        "artifact_count": len(artifacts),
        "updated_artifacts": updated_artifacts,
        "skipped_artifacts": skipped_artifacts,
        "artifacts_with_ocr": with_ocr,
        "updated_segments": updated_segments,
        "failed": failed,
        "stage2": stage2_summary,
    }
    print(json_summary(summary), flush=True)
    return summary


def json_summary(summary: dict) -> str:
    import json

    return json.dumps(
        {key: value for key, value in summary.items() if key != "failed"}
        | {"failed_count": len(summary.get("failed") or [])},
        indent=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=OP_ROOT / "data" / "output" / "training_video_day2",
        help="Training video output root containing stage_1_source_bundle/",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-OCR every artifact, including ones already read by azure_cv",
    )
    parser.add_argument(
        "--skip-stage2",
        action="store_true",
        help="Only update Stage 1 JSON; do not re-run Stage 2 preparer",
    )
    args = parser.parse_args()
    summary = backfill_source_root(
        args.source_root.resolve(),
        force=args.force,
        run_stage2=not args.skip_stage2,
    )
    if summary["failed"]:
        print("Failures:", flush=True)
        for item in summary["failed"]:
            print(f"  - {item}", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
