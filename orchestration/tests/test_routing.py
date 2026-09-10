"""Routing unit tests for the ingestion orchestrator."""

from __future__ import annotations

from pathlib import Path

from orchestration.routing import classify_upload, extract_case_id, is_ingestible_file


def test_extract_case_id() -> None:
    assert extract_case_id("Case 228086 Data.pdf") == "228086"
    assert extract_case_id("case_228723.zip") == "228723"
    assert extract_case_id("manual.pdf") is None


def test_classify_incident_by_name(tmp_path: Path) -> None:
    pdf = tmp_path / "Case 228086 Data.pdf"
    pdf.write_bytes(b"%PDF")
    routed = classify_upload(pdf)
    assert routed.source_type == "incident"
    assert routed.case_id == "228086"


def test_classify_manual_pdf(tmp_path: Path) -> None:
    pdf = tmp_path / "OptiSweep Operation Manual.pdf"
    pdf.write_bytes(b"%PDF")
    routed = classify_upload(pdf)
    assert routed.source_type == "manual"


def test_classify_training_video_with_vtt(tmp_path: Path) -> None:
    video = tmp_path / "training_day1.mp4"
    vtt = tmp_path / "training_day1.vtt"
    video.write_bytes(b"0")
    vtt.write_text("WEBVTT\n")
    routed = classify_upload(video)
    assert routed.source_type == "training_video"
    assert vtt.resolve() in routed.companion_paths


def test_is_ingestible_file(tmp_path: Path) -> None:
    pdf = tmp_path / "a.pdf"
    vtt = tmp_path / "a.vtt"
    pdf.write_bytes(b"%PDF")
    vtt.write_text("WEBVTT\n")
    assert is_ingestible_file(pdf)
    assert not is_ingestible_file(vtt)
