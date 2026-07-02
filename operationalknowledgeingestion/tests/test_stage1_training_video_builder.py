from pathlib import Path
import subprocess
import tempfile

from optisweep_ingestion.stage1_training_video_builder import (
    CropBox,
    FrameSample,
    SlideInterval,
    TesseractOCRClient,
    align_cues_to_intervals,
    build_segmentation_quality_report,
    detect_slide_intervals_from_samples,
    format_timecode,
    normalize_ocr_text,
    ocr_text_changed,
    parse_crop_box,
    parse_timecode,
    parse_vtt,
    validate_training_video_outputs,
)


def test_timecode_round_trip() -> None:
    assert parse_timecode("01:48:58.000") == 6538.0
    assert format_timecode(6538.0) == "01:48:58.000"


def test_parse_crop_box() -> None:
    box = parse_crop_box("0,68,1676,1012")
    assert box == CropBox(0, 68, 1676, 1012)
    assert box.width == 1676
    assert box.height == 944


def test_parse_vtt_preserves_cues(tmp_path: Path) -> None:
    path = tmp_path / "sample.vtt"
    path.write_text(
        """WEBVTT

cue-a
00:00:01.000 --> 00:00:02.500
Hello <c>world</c>.

00:00:03.000 --> 00:00:04.000
Second cue.
""",
        encoding="utf-8",
    )

    cues = parse_vtt(path)

    assert len(cues) == 2
    assert cues[0].cue_id == "cue-a"
    assert cues[0].start_timecode == "00:00:01.000"
    assert cues[0].text == "Hello world."
    assert cues[1].cue_id == "cue_00002"


def test_align_cues_prefers_greatest_actual_overlap() -> None:
    intervals = [
        SlideInterval(index=1, start_time_seconds=0, end_time_seconds=10, confidence="high"),
        SlideInterval(index=2, start_time_seconds=8, end_time_seconds=20, confidence="high"),
    ]
    cues = parse_vtt(
        _write_vtt(
            """WEBVTT

cue-1
00:00:09.000 --> 00:00:12.000
Overlaps both.
"""
        )
    )

    assignments, warnings = align_cues_to_intervals(cues, intervals)

    assert warnings == []
    assert assignments["segment_training_video_0001"] == []
    assert assignments["segment_training_video_0002"][0]["cue_id"] == "cue-1"
    assert assignments["segment_training_video_0002"][0]["alignment_type"] == "exact_overlap"


def test_align_cues_uses_buffer_and_nearest_slide() -> None:
    intervals = [
        SlideInterval(index=1, start_time_seconds=10, end_time_seconds=20, confidence="high"),
        SlideInterval(index=2, start_time_seconds=30, end_time_seconds=40, confidence="high"),
    ]
    cues = parse_vtt(
        _write_vtt(
            """WEBVTT

cue-buffer
00:00:20.500 --> 00:00:21.000
Buffered.

cue-nearest
00:00:25.000 --> 00:00:25.500
Nearest.
"""
        )
    )

    assignments, warnings = align_cues_to_intervals(cues, intervals, buffer_before_seconds=1.5, buffer_after_seconds=3.0)

    assert assignments["segment_training_video_0001"][0]["alignment_type"] == "buffered_overlap"
    assert assignments["segment_training_video_0002"][0]["alignment_type"] == "nearest_slide"
    assert warnings[0]["cue_id"] == "cue-nearest"


def test_validate_training_video_outputs_catches_linked_ids_and_missing_artifacts() -> None:
    artifacts = [
        {
            "artifact_id": "artifact_1",
            "source_id": "source_1",
            "source_type": "training_video",
            "ingestion_batch_id": "batch_1",
            "source_refs": [{"source_id": "source_1"}],
            "linked_context_ids": ["ctx_1"],
            "linked_runbook_ids": [],
            "ocr_text": "",
            "ocr_provenance": None,
        }
    ]
    segments = [
        {
            "segment_id": "segment_1",
            "source_id": "source_1",
            "source_type": "training_video",
            "ingestion_batch_id": "batch_1",
            "source_refs": [{"source_id": "source_1"}],
            "representative_artifact_id": "missing",
            "artifact_ids": ["artifact_1"],
            "transcript_cues": [{"alignment_type": "exact_overlap"}],
        }
    ]

    errors = validate_training_video_outputs(segments, artifacts)

    assert any("linked_context_ids" in error for error in errors)
    assert any("representative artifact does not exist" in error for error in errors)


def test_tesseract_ocr_client_parses_tsv(monkeypatch, tmp_path: Path) -> None:
    image = tmp_path / "sample.jpg"
    image.write_bytes(b"fake")

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=(
                "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
                "5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t92\tCharger\n"
                "5\t1\t1\t1\t1\t2\t10\t0\t10\t10\t88\tSelection\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = TesseractOCRClient(command="tesseract").extract(image)

    assert result.text == "Charger Selection"
    assert result.confidence == 90.0
    assert result.provenance["backend"] == "tesseract"


def test_ocr_text_normalization_and_change_detection() -> None:
    assert normalize_ocr_text("Charger   Selection!") == "charger selection"
    assert not ocr_text_changed("Charger Selection disable charger", "Charger Selection disable charger manually")
    assert ocr_text_changed("Charger Selection disable charger", "AGV API page remove robot")


def test_detect_slide_intervals_does_not_split_on_ocr_noise_without_visual_support() -> None:
    samples = [
        _sample(0, "Overview What is Optisweep", 0.0),
        _sample(3, "Overview What is Optisweep", 0.5),
        _sample(6, "Charger Selection disable charger", 0.5),
        _sample(9, "Charger Selection disable charger", 0.5),
    ]

    intervals = detect_slide_intervals_from_samples(
        frame_samples=samples,
        duration_seconds=12,
        slide_change_threshold=18,
        min_segment_seconds=3,
        max_segment_seconds=120,
    )

    assert len(intervals) == 1


def test_detect_slide_intervals_splits_on_ocr_change_with_visual_support() -> None:
    samples = [
        _sample(0, "Overview What is Optisweep", 0.0),
        _sample(3, "Overview What is Optisweep", 0.5),
        _sample(6, "Charger Selection disable charger", 12.0),
        _sample(9, "Charger Selection disable charger", 0.5),
    ]

    intervals = detect_slide_intervals_from_samples(
        frame_samples=samples,
        duration_seconds=12,
        slide_change_threshold=18,
        min_segment_seconds=3,
        max_segment_seconds=120,
    )

    assert len(intervals) == 2
    assert intervals[1].start_time_seconds == 6
    assert "ocr_text_change_with_visual_support" in intervals[1].segmentation_reasons


def test_detect_slide_intervals_does_not_split_stable_ocr_and_visuals() -> None:
    samples = [
        _sample(0, "Overview What is Optisweep", 0.0),
        _sample(3, "Overview What is Optisweep", 0.5),
        _sample(6, "Overview What is Optisweep software", 0.5),
    ]

    intervals = detect_slide_intervals_from_samples(
        frame_samples=samples,
        duration_seconds=9,
        slide_change_threshold=18,
        min_segment_seconds=3,
        max_segment_seconds=120,
    )

    assert len(intervals) == 1


def test_quality_report_flags_long_segments() -> None:
    intervals = [SlideInterval(index=1, start_time_seconds=0, end_time_seconds=130, confidence="medium")]
    report = build_segmentation_quality_report(intervals, {"segment_training_video_0001": []}, max_segment_seconds=120)

    assert report["low_quality"] is True
    assert report["long_segment_count"] == 1


def test_validate_allows_ocr_when_enabled() -> None:
    artifacts = [
        {
            "artifact_id": "artifact_1",
            "source_id": "source_1",
            "source_type": "training_video",
            "ingestion_batch_id": "batch_1",
            "source_refs": [{"source_id": "source_1"}],
            "linked_context_ids": [],
            "linked_runbook_ids": [],
            "ocr_text": "Charger Selection",
            "ocr_provenance": {"backend": "tesseract"},
        }
    ]
    segments = [
        {
            "segment_id": "segment_1",
            "source_id": "source_1",
            "source_type": "training_video",
            "ingestion_batch_id": "batch_1",
            "source_refs": [{"source_id": "source_1"}],
            "representative_artifact_id": "artifact_1",
            "artifact_ids": ["artifact_1"],
            "transcript_cues": [{"alignment_type": "exact_overlap"}],
        }
    ]

    assert validate_training_video_outputs(segments, artifacts, ocr_enabled=True) == []


def _sample(seconds: float, text: str, diff: float) -> FrameSample:
    return FrameSample(
        timestamp_seconds=seconds,
        timestamp_timecode=format_timecode(seconds),
        diff_from_previous=diff,
        diff_from_last_cut=diff,
        ocr_text=text,
        ocr_confidence=90.0,
        ocr_text_hash="hash",
        detected_title=text.split()[0],
        ocr_provenance={"backend": "tesseract"},
    )


def _write_vtt(text: str) -> Path:
    directory = Path(tempfile.mkdtemp(prefix="training_video_builder_"))
    path = directory / "test_alignment.vtt"
    path.write_text(text, encoding="utf-8")
    return path
