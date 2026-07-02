"""Prepare training-video bundle outputs for shared Stage 3/4/5 extractors."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from optisweep_ingestion.services.id_generator import slugify
from optisweep_ingestion.utils.json_utils import read_json, write_json


def prepare_training_video_for_extraction(
    training_segments_path: str | Path,
    source_artifacts_path: str | Path,
    output_dir: str | Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    segments = read_json(training_segments_path)
    artifacts = read_json(source_artifacts_path)
    if not isinstance(segments, list):
        raise ValueError("training_video_slide_segments.json must contain a list.")
    if not isinstance(artifacts, list):
        raise ValueError("source_artifacts.json must contain a list.")
    if not segments:
        raise ValueError("training_video_slide_segments.json must contain at least one segment.")

    first = segments[0]
    source_id = str(first.get("source_id") or "training_video")
    source_title = str(first.get("source_title") or source_id)
    source_version = first.get("source_version")
    ingestion_batch_id = str(first.get("ingestion_batch_id") or f"batch_{source_id}")
    source_document_id = f"{slugify(source_id)}_video"
    source_bundle_id = f"{slugify(source_id)}_bundle"

    pages: list[dict[str, Any]] = []
    sections: list[dict[str, Any]] = []
    segment_section_lookup: dict[str, str] = {}
    for index, segment in enumerate(segments, start=1):
        section_id = f"{slugify(source_id)}_segment_{index:04d}"
        segment_id = str(segment.get("segment_id") or section_id)
        segment_section_lookup[segment_id] = section_id
        text = _clean_text(_segment_text(segment))
        source_refs = _segment_source_refs(segment, source_id, ingestion_batch_id, source_document_id, section_id)
        pages.append(
            {
                "page_number": index,
                "text": text,
                "text_length": len(text),
                "section_id": section_id,
                "section_ids": [section_id],
                "unit_type": "training_video_slide_segment",
                "segment_id": segment_id,
                "start_time_seconds": segment.get("start_time_seconds"),
                "end_time_seconds": segment.get("end_time_seconds"),
                "start_timecode": segment.get("start_timecode"),
                "end_timecode": segment.get("end_timecode"),
                "source_refs": source_refs,
            }
        )
        sections.append(
            {
                "section_id": section_id,
                "title": _section_title(segment, index),
                "level": 1,
                "page_start": index,
                "page_end": index,
                "parent_section_id": None,
                "text_preview": text[:500],
                "unit_type": "training_video_slide_segment",
                "segment_id": segment_id,
                "start_time_seconds": segment.get("start_time_seconds"),
                "end_time_seconds": segment.get("end_time_seconds"),
                "start_timecode": segment.get("start_timecode"),
                "end_timecode": segment.get("end_timecode"),
                "source_refs": source_refs,
            }
        )

    prepared_artifacts = [
        _prepare_artifact(
            artifact,
            source_document_id=source_document_id,
            source_bundle_id=source_bundle_id,
            segment_section_lookup=segment_section_lookup,
            segments=segments,
        )
        for artifact in artifacts
    ]

    source_bundle = {
        "source_bundle_id": source_bundle_id,
        "source_metadata": {
            "source_id": source_id,
            "source_type": "training_video",
            "source_title": source_title,
            "source_version": source_version,
            "ingestion_batch_id": ingestion_batch_id,
            "source_document_id": source_document_id,
        },
        "source_document": {
            "source_document_id": source_document_id,
            "title": source_title,
            "document_type": "training_video",
            "version": source_version,
            "document_date": None,
            "source_type": "training_video",
            "source_path": str(first.get("source_refs", [{}])[0].get("source_id") or source_id),
        },
        "pages": pages,
        "sections": sections,
        "figure_refs": [],
        "table_refs": [],
        "build_metadata": {
            "created_by": "training_video_preparer",
            "input_training_segments": str(training_segments_path),
            "input_source_artifacts": str(source_artifacts_path),
        },
    }

    report = {
        "input_training_segments": str(training_segments_path),
        "input_source_artifacts": str(source_artifacts_path),
        "source_bundle": str(Path(output_dir) / "source_bundle.json"),
        "source_artifacts": str(Path(output_dir) / "source_artifacts.json"),
        "source_artifacts_enriched": str(Path(output_dir) / "source_artifacts_enriched.json"),
        "artifact_extraction_report": str(Path(output_dir) / "artifact_extraction_report.json"),
        "segment_count": len(segments),
        "page_count": len(pages),
        "section_count": len(sections),
        "artifact_count": len(prepared_artifacts),
        "artifacts_with_section_id": sum(1 for artifact in prepared_artifacts if artifact.get("section_id")),
        "warnings": _report_warnings(segments, prepared_artifacts),
    }
    artifact_report = _artifact_extraction_report(
        source_artifacts_path=source_artifacts_path,
        source_bundle_id=source_bundle_id,
        source_document_id=source_document_id,
        artifacts=prepared_artifacts,
        segments=segments,
    )

    output_path = Path(output_dir)
    write_json(output_path / "source_bundle.json", source_bundle)
    write_json(output_path / "source_artifacts.json", prepared_artifacts)
    write_json(output_path / "source_artifacts_enriched.json", prepared_artifacts)
    write_json(output_path / "artifact_extraction_report.json", artifact_report)
    write_json(output_path / "training_video_preparation_report.json", report)
    return source_bundle, prepared_artifacts, report


def _segment_text(segment: dict[str, Any]) -> str:
    title = _clean_text(str(segment.get("title") or "").strip())
    transcript = _clean_text(str(segment.get("transcript_text") or "").strip())
    ocr = _clean_text(str(segment.get("ocr_text") or "").strip())
    parts = [
        f"Training video slide segment: {title}" if title else "Training video slide segment.",
        f"Timestamp: {segment.get('start_timecode')} to {segment.get('end_timecode')}.",
    ]
    if transcript:
        parts.append(f"Transcript: {transcript}")
    if ocr:
        parts.append(f"OCR text: {ocr}")
    artifact_ids = segment.get("artifact_ids") or []
    if artifact_ids:
        parts.append("Related artifact IDs: " + ", ".join(str(item) for item in artifact_ids))
    return "\n".join(parts).strip()


def _section_title(segment: dict[str, Any], index: int) -> str:
    title = _clean_text(str(segment.get("title") or "").strip())
    timecode = str(segment.get("start_timecode") or "")
    if title:
        return f"Training Video Segment {index:04d}: {title}"
    return f"Training Video Segment {index:04d}: {timecode}"


def _segment_source_refs(
    segment: dict[str, Any],
    source_id: str,
    ingestion_batch_id: str,
    source_document_id: str,
    section_id: str,
) -> list[dict[str, Any]]:
    refs = segment.get("source_refs") or []
    if not refs:
        refs = [
            {
                "source_id": source_id,
                "source_type": "training_video",
                "ingestion_batch_id": ingestion_batch_id,
                "timestamp_start": segment.get("start_timecode"),
                "timestamp_end": segment.get("end_timecode"),
                "start_time_seconds": segment.get("start_time_seconds"),
                "end_time_seconds": segment.get("end_time_seconds"),
            }
        ]
    normalized = []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        updated = dict(ref)
        updated.setdefault("source_id", source_id)
        updated.setdefault("source_type", "training_video")
        updated.setdefault("ingestion_batch_id", ingestion_batch_id)
        updated["source_document_id"] = source_document_id
        updated["section_id"] = section_id
        normalized.append(updated)
    return normalized


def _prepare_artifact(
    artifact: dict[str, Any],
    *,
    source_document_id: str,
    source_bundle_id: str,
    segment_section_lookup: dict[str, str],
    segments: list[dict[str, Any]],
) -> dict[str, Any]:
    updated = _clean_record(dict(artifact))
    segment_id = str(updated.get("segment_id") or "")
    section_id = segment_section_lookup.get(segment_id)
    segment = next((item for item in segments if item.get("segment_id") == segment_id), None)
    page_number = segments.index(segment) + 1 if segment in segments else None
    if section_id:
        updated["section_id"] = section_id
    if page_number:
        updated["page_number"] = page_number
    updated["source_document_id"] = source_document_id
    updated["source_bundle_id"] = source_bundle_id
    updated.setdefault("detailed_description", updated.get("summary") or updated.get("short_description") or "")
    updated.setdefault("tags", [])
    updated.setdefault("enrichment_notes", [])
    updated.setdefault("linked_procedure_ids", [])
    updated["linked_context_ids"] = []
    updated["linked_runbook_ids"] = []
    if segment:
        transcript = _clean_text(str(segment.get("transcript_text") or "").strip())
        current_retrieval = _clean_text(str(updated.get("retrieval_text") or "").strip())
        if transcript and transcript not in current_retrieval:
            updated["retrieval_text"] = f"{current_retrieval} Transcript near this frame: {transcript[:800]}".strip()
        updated["nearby_text"] = transcript
        updated["caption_text"] = _clean_text(str(segment.get("title") or ""))
    return updated


def _artifact_extraction_report(
    *,
    source_artifacts_path: str | Path,
    source_bundle_id: str,
    source_document_id: str,
    artifacts: list[dict[str, Any]],
    segments: list[dict[str, Any]],
) -> dict[str, Any]:
    artifacts_with_images = sum(1 for artifact in artifacts if artifact.get("storage_path"))
    artifacts_with_ocr = sum(1 for artifact in artifacts if artifact.get("ocr_text"))
    artifacts_with_transcript = sum(1 for artifact in artifacts if artifact.get("nearby_text"))
    return {
        "stage": "stage_2_video_source_artifact_preparation",
        "source_type": "training_video",
        "input_source_artifacts": str(source_artifacts_path),
        "source_bundle_id": source_bundle_id,
        "source_document_id": source_document_id,
        "input_artifact_count": len(artifacts),
        "extracted_artifact_count": len(artifacts),
        "written_artifact_count": len(artifacts),
        "segment_count": len(segments),
        "artifacts_with_images": artifacts_with_images,
        "artifacts_with_ocr": artifacts_with_ocr,
        "artifacts_with_transcript": artifacts_with_transcript,
        "skipped_artifact_count": 0,
        "failed_artifact_count": 0,
        "warnings": _report_warnings(segments, artifacts),
        "notes": [
            "Training video artifacts are representative slide-frame captures produced by Video Phase 1.",
            "This report mirrors the manual Stage 2 artifact extraction contract for Stage 3 compatibility.",
        ],
    }


def _clean_record(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _clean_record(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clean_record(item) for item in value]
    if isinstance(value, str):
        return _clean_text(value)
    return value


def _clean_text(value: str) -> str:
    replacements = {
        "\u00a2": "c",
        "\u00ae": "",
        "\u00a9": "",
        "\u00c2": "",
        "Â¢": "c",
        "Â®": "",
        "Â©": "",
        "Â": "",
        "â€™": "'",
        "â€œ": '"',
        "â€": '"',
        "â€“": "-",
        "â€”": "-",
        "â€¦": "...",
    }
    cleaned = value
    for bad, good in replacements.items():
        cleaned = cleaned.replace(bad, good)
    return cleaned.strip()


def _report_warnings(segments: list[dict[str, Any]], artifacts: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if any(not str(segment.get("transcript_text") or "").strip() for segment in segments):
        warnings.append("One or more segments have no aligned transcript text.")
    if any(not artifact.get("section_id") for artifact in artifacts):
        warnings.append("One or more artifacts could not be assigned to a video segment section.")
    if any(artifact.get("ocr_text") for artifact in artifacts):
        warnings.append("OCR text is present on at least one artifact; verify OCR provenance before downstream use.")
    return warnings
