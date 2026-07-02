from pathlib import Path

from optisweep_ingestion.services.source_ref_service import lineage_from_bundle
from optisweep_ingestion.stage4_operational_context import build_source_packets
from optisweep_ingestion.stage5_runbook_candidates import build_candidate_packets
from optisweep_ingestion.stage2_training_video_preparer import prepare_training_video_for_extraction
from optisweep_ingestion.utils.json_utils import write_json


def test_prepare_training_video_writes_source_bundle_compatible_records(tmp_path: Path) -> None:
    segments_path, artifacts_path = _write_inputs(tmp_path)

    bundle, artifacts, report = prepare_training_video_for_extraction(
        training_segments_path=segments_path,
        source_artifacts_path=artifacts_path,
        output_dir=tmp_path,
    )

    assert bundle["source_metadata"]["source_type"] == "training_video"
    assert bundle["pages"][0]["text_length"] > 0
    assert bundle["sections"][0]["section_id"] == "training_video_day1_segment_0001"
    assert bundle["sections"][0]["source_refs"][0]["timestamp_start"] == "00:01:00.000"
    assert artifacts[0]["section_id"] == "training_video_day1_segment_0001"
    assert artifacts[0]["page_number"] == 1
    assert artifacts[0]["linked_context_ids"] == []
    assert artifacts[0]["ocr_text"] == "Charger Selection"
    assert artifacts[0]["ocr_provenance"]["backend"] == "tesseract"
    assert "OCR text: Charger Selection" in bundle["pages"][0]["text"]
    assert report["segment_count"] == 1
    assert (tmp_path / "source_bundle.json").exists()
    assert (tmp_path / "source_artifacts_enriched.json").exists()


def test_stage4_packets_include_training_video_segments_and_timestamp_refs(tmp_path: Path) -> None:
    segments_path, artifacts_path = _write_inputs(tmp_path)
    bundle, artifacts, _ = prepare_training_video_for_extraction(segments_path, artifacts_path, tmp_path)
    lineage = lineage_from_bundle(bundle)

    packets = build_source_packets(bundle, artifacts, lineage)

    assert len(packets) == 1
    assert packets[0]["source_type"] == "training_video"
    assert "Transcript:" in packets[0]["section_text"]
    assert packets[0]["source_refs"][0]["timestamp_start"] == "00:01:00.000"
    assert packets[0]["related_artifacts"][0]["artifact_id"] == "artifact_training_video_1"


def test_stage5_packets_include_training_video_segments(tmp_path: Path) -> None:
    segments_path, artifacts_path = _write_inputs(tmp_path)
    bundle, artifacts, _ = prepare_training_video_for_extraction(segments_path, artifacts_path, tmp_path)
    lineage = lineage_from_bundle(bundle)
    contexts = [
        {
            "context_id": "ctx_training_video_charger_selection",
            "title": "Charger Selection",
            "context_type": "operation_reference",
            "summary": "Charger selection guidance.",
            "details": "The segment discusses disabling a charger.",
            "retrieval_text": "Charger selection disable charger AGV.",
            "related_artifact_ids": ["artifact_training_video_1"],
            "source_refs": bundle["sections"][0]["source_refs"],
            "validation_status": "needs_sme_review",
        }
    ]

    packets = build_candidate_packets(bundle, artifacts, contexts, lineage)

    assert len(packets) == 1
    assert packets[0]["related_operational_context"][0]["context_id"] == "ctx_training_video_charger_selection"
    assert packets[0]["source_refs"][0]["timestamp_start"] == "00:01:00.000"


def _write_inputs(tmp_path: Path) -> tuple[Path, Path]:
    segments = [
        {
            "segment_id": "segment_training_video_0001",
            "unit_type": "training_video_slide_segment",
            "source_id": "training_video_day1",
            "source_type": "training_video",
            "source_title": "Training Day 1",
            "source_version": None,
            "ingestion_batch_id": "batch_training_video_day1",
            "title": "Charger Selection",
            "start_time_seconds": 60.0,
            "end_time_seconds": 90.0,
            "start_timecode": "00:01:00.000",
            "end_timecode": "00:01:30.000",
            "representative_artifact_id": "artifact_training_video_1",
            "artifact_ids": ["artifact_training_video_1"],
            "transcript_cues": [],
            "transcript_text": "When charger selection is selected, select a charger to view charger information.",
            "ocr_text": "Charger Selection",
            "ocr_confidence": 91.0,
            "ocr_provenance": {"backend": "tesseract", "confidence": 91.0},
            "ocr_text_hash": "abc123",
            "detected_title": "Charger Selection",
            "combined_text": "When charger selection is selected, select a charger to view charger information.\nCharger Selection",
            "source_refs": [
                {
                    "source_id": "training_video_day1",
                    "source_type": "training_video",
                    "ingestion_batch_id": "batch_training_video_day1",
                    "timestamp_start": "00:01:00.000",
                    "timestamp_end": "00:01:30.000",
                    "start_time_seconds": 60.0,
                    "end_time_seconds": 90.0,
                    "segment_id": "segment_training_video_0001",
                }
            ],
            "confidence": "high",
            "warnings": [],
            "validation_status": "needs_sme_review",
        }
    ]
    artifacts = [
        {
            "artifact_id": "artifact_training_video_1",
            "artifact_type": "training_video_slide_frame",
            "image_type": "training_video_frame",
            "source_id": "training_video_day1",
            "source_type": "training_video",
            "source_title": "Training Day 1",
            "source_version": None,
            "ingestion_batch_id": "batch_training_video_day1",
            "segment_id": "segment_training_video_0001",
            "timestamp_seconds": 75.0,
            "timestamp_timecode": "00:01:15.000",
            "storage_path": "images/artifact_training_video_1.jpg",
            "file_name": "artifact_training_video_1.jpg",
            "title": "Charger Selection",
            "short_description": "Captured training video slide frame.",
            "summary": "Captured charger selection training slide.",
            "retrieval_text": "Training video slide frame captured at 00:01:15.000.",
            "what_to_look_at": [],
            "ocr_text": "Charger Selection",
            "ocr_confidence": 91.0,
            "ocr_provenance": {"backend": "tesseract", "confidence": 91.0},
            "ocr_text_hash": "abc123",
            "detected_title": "Charger Selection",
            "source_refs": [],
            "linked_context_ids": [],
            "linked_runbook_ids": [],
            "validation_status": "needs_sme_review",
        }
    ]
    segments_path = tmp_path / "training_video_slide_segments.json"
    artifacts_path = tmp_path / "source_artifacts.json"
    write_json(segments_path, segments)
    write_json(artifacts_path, artifacts)
    return segments_path, artifacts_path
