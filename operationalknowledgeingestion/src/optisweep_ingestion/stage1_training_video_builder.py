"""Build normalized source records from a training video plus VTT transcript."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any

from optisweep_ingestion.services.id_generator import slugify
from optisweep_ingestion.utils.json_utils import write_json


@dataclass(frozen=True)
class CropBox:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    def as_dict(self) -> dict[str, int]:
        return {
            "left": self.left,
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class TranscriptCue:
    cue_id: str
    start_time_seconds: float
    end_time_seconds: float
    start_timecode: str
    end_timecode: str
    text: str
    raw_text: str | None = None


@dataclass
class SlideInterval:
    index: int
    start_time_seconds: float
    end_time_seconds: float
    confidence: str
    detection_method: str = "cropped_frame_similarity"
    warnings: list[str] = field(default_factory=list)
    segmentation_reasons: list[str] = field(default_factory=list)
    ocr_text: str = ""
    ocr_confidence: float | None = None
    ocr_provenance: dict[str, Any] | None = None
    ocr_text_hash: str | None = None
    detected_title: str | None = None

    @property
    def segment_id(self) -> str:
        return f"segment_training_video_{self.index:04d}"

    @property
    def start_timecode(self) -> str:
        return format_timecode(self.start_time_seconds)

    @property
    def end_timecode(self) -> str:
        return format_timecode(self.end_time_seconds)


def parse_crop_box(value: str) -> CropBox:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("Crop box must use left,top,right,bottom.")
    left, top, right, bottom = [int(part) for part in parts]
    box = CropBox(left=left, top=top, right=right, bottom=bottom)
    if box.width <= 0 or box.height <= 0:
        raise ValueError("Crop box right/bottom must be greater than left/top.")
    return box


def parse_timecode(value: str) -> float:
    text = value.strip().replace(",", ".")
    parts = text.split(":")
    if len(parts) == 2:
        hours = 0
        minutes = int(parts[0])
        seconds = float(parts[1])
    elif len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
    else:
        raise ValueError(f"Unsupported VTT timecode: {value}")
    return hours * 3600 + minutes * 60 + seconds


def format_timecode(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float | None
    backend: str | None
    provenance: dict[str, Any] | None


@dataclass(frozen=True)
class FrameSample:
    timestamp_seconds: float
    timestamp_timecode: str
    diff_from_previous: float | None
    diff_from_last_cut: float | None
    ocr_text: str = ""
    ocr_confidence: float | None = None
    ocr_text_hash: str | None = None
    detected_title: str | None = None
    ocr_provenance: dict[str, Any] | None = None


class TesseractOCRClient:
    def __init__(self, command: str | None = None) -> None:
        self.command = command or os.getenv("TESSERACT_CMD") or "tesseract"

    def extract(self, image_path: str | Path) -> OCRResult:
        image = Path(image_path)
        command = [self.command, str(image), "stdout", "--psm", "6", "tsv"]
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Tesseract is not available. Install Tesseract or set TESSERACT_CMD."
            ) from exc
        except subprocess.CalledProcessError as exc:
            details = (exc.stderr or exc.stdout or "").strip()
            raise RuntimeError(f"Tesseract OCR failed: {details}") from exc
        words: list[str] = []
        confidences: list[float] = []
        for line in completed.stdout.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) < 12:
                continue
            text = parts[11].strip()
            if not text:
                continue
            words.append(text)
            try:
                confidence = float(parts[10])
            except ValueError:
                continue
            if confidence >= 0:
                confidences.append(confidence)
        confidence_value = round(sum(confidences) / len(confidences), 2) if confidences else None
        return OCRResult(
            text=" ".join(words).strip(),
            confidence=confidence_value,
            backend="tesseract",
            provenance={
                "backend": "tesseract",
                "command": self.command,
                "source_image_path": str(image),
                "confidence": confidence_value,
            },
        )


def normalize_ocr_text(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9\s]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def ocr_text_hash(text: str) -> str | None:
    normalized = normalize_ocr_text(text)
    if not normalized:
        return None
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def detect_title_from_ocr(text: str) -> str | None:
    for line in re.split(r"[\r\n]+| {3,}", text):
        cleaned = re.sub(r"\s+", " ", line).strip(" -•\t")
        if 3 <= len(cleaned) <= 90 and re.search(r"[A-Za-z]", cleaned):
            return cleaned
    words = normalize_ocr_text(text).split()
    return " ".join(words[:8]) if words else None


def ocr_text_changed(previous: str, current: str, min_similarity: float = 0.72) -> bool:
    previous_tokens = set(normalize_ocr_text(previous).split())
    current_tokens = set(normalize_ocr_text(current).split())
    if not previous_tokens or not current_tokens:
        return False
    overlap = len(previous_tokens & current_tokens)
    similarity = overlap / max(len(previous_tokens), len(current_tokens))
    return similarity < min_similarity


def parse_vtt(path: str | Path) -> list[TranscriptCue]:
    text = Path(path).read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.strip())
    cues: list[TranscriptCue] = []
    cue_index = 1
    timestamp_re = re.compile(
        r"(?P<start>\d{2}:\d{2}(?::\d{2})?[\.,]\d{3})\s+-->\s+"
        r"(?P<end>\d{2}:\d{2}(?::\d{2})?[\.,]\d{3})"
    )
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if not lines or lines[0].strip().upper() == "WEBVTT":
            continue
        timestamp_index = next((idx for idx, line in enumerate(lines) if timestamp_re.search(line)), None)
        if timestamp_index is None:
            continue
        match = timestamp_re.search(lines[timestamp_index])
        if match is None:
            continue
        cue_id = lines[timestamp_index - 1] if timestamp_index > 0 else f"cue_{cue_index:05d}"
        cue_text_lines = lines[timestamp_index + 1 :]
        cue_text = " ".join(_clean_vtt_text(line) for line in cue_text_lines).strip()
        cues.append(
            TranscriptCue(
                cue_id=cue_id,
                start_time_seconds=parse_timecode(match.group("start")),
                end_time_seconds=parse_timecode(match.group("end")),
                start_timecode=match.group("start").replace(",", "."),
                end_timecode=match.group("end").replace(",", "."),
                text=cue_text,
                raw_text="\n".join(cue_text_lines) if cue_text_lines else None,
            )
        )
        cue_index += 1
    return cues


def align_cues_to_intervals(
    cues: list[TranscriptCue],
    intervals: list[SlideInterval],
    buffer_before_seconds: float = 1.5,
    buffer_after_seconds: float = 3.0,
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    assignments: dict[str, list[dict[str, Any]]] = {interval.segment_id: [] for interval in intervals}
    warnings: list[dict[str, Any]] = []
    if not intervals:
        return assignments, [{"warning": "No slide intervals detected; transcript cues could not be aligned."}]

    for cue in cues:
        candidates: list[dict[str, Any]] = []
        for interval in intervals:
            actual_overlap = _overlap_seconds(
                cue.start_time_seconds,
                cue.end_time_seconds,
                interval.start_time_seconds,
                interval.end_time_seconds,
            )
            buffered_overlap = _overlap_seconds(
                cue.start_time_seconds,
                cue.end_time_seconds,
                interval.start_time_seconds - buffer_before_seconds,
                interval.end_time_seconds + buffer_after_seconds,
            )
            if actual_overlap > 0:
                alignment_type = "exact_overlap"
                confidence = "high"
            elif buffered_overlap > 0:
                alignment_type = "buffered_overlap"
                confidence = "medium"
            else:
                continue
            candidates.append(
                {
                    "interval": interval,
                    "alignment_type": alignment_type,
                    "overlap_seconds": actual_overlap,
                    "buffered_overlap_seconds": buffered_overlap,
                    "alignment_confidence": confidence,
                }
            )
        if candidates:
            selected = _select_best_alignment(candidates)
        else:
            nearest = min(intervals, key=lambda item: _distance_to_interval(cue, item))
            selected = {
                "interval": nearest,
                "alignment_type": "nearest_slide",
                "overlap_seconds": 0.0,
                "buffered_overlap_seconds": 0.0,
                "alignment_confidence": "low",
            }
            warnings.append(
                {
                    "cue_id": cue.cue_id,
                    "warning": "Cue did not overlap any detected slide interval or buffer; assigned to nearest slide.",
                    "assigned_segment_id": nearest.segment_id,
                }
            )
        interval = selected["interval"]
        assignments[interval.segment_id].append(_aligned_cue_record(cue, selected))
    return assignments, warnings


def build_training_video_bundle(
    source_video: str | Path,
    transcript_vtt: str | Path,
    output_dir: str | Path,
    source_id: str | None = None,
    source_title: str | None = None,
    source_version: str | None = None,
    ingestion_batch_id: str | None = None,
    crop_box: CropBox | None = None,
    sampling_interval_seconds: float = 1.0,
    slide_change_threshold: float = 18.0,
    min_segment_seconds: float = 3.0,
    buffer_before_seconds: float = 1.5,
    buffer_after_seconds: float = 3.0,
    extra_frame_threshold: float = 8.0,
    max_extra_frames_per_segment: int = 0,
    ocr_backend: str = "none",
    tesseract_command: str | None = None,
    sample_ocr_interval_seconds: float = 3.0,
    max_segment_seconds: float = 120.0,
    max_duration_seconds: float | None = None,
    duplicate_slide_merge_threshold: float = 3.0,
    write_segmentation_inspection: bool = False,
    fail_on_low_quality_segmentation: bool = False,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    cv2 = _load_cv2()
    video_path = Path(source_video)
    vtt_path = Path(transcript_vtt)
    output_path = Path(output_dir)
    images_dir = output_path / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0.0
    if max_duration_seconds is not None and max_duration_seconds > 0:
        duration = min(duration, max_duration_seconds)
    if crop_box is None:
        crop_box = CropBox(0, 0, width, height)
    _validate_crop_box(crop_box, width, height)

    source_id = source_id or slugify(video_path.stem)
    source_title = source_title or video_path.stem
    ingestion_batch_id = ingestion_batch_id or f"batch_{source_id}"

    ocr_client = _build_ocr_client(ocr_backend, tesseract_command)
    samples_dir = output_path / "segmentation_samples"
    frame_samples = collect_frame_samples(
        cap=cap,
        duration_seconds=duration,
        fps=fps,
        crop_box=crop_box,
        sampling_interval_seconds=sampling_interval_seconds,
        slide_change_threshold=slide_change_threshold,
        ocr_client=ocr_client,
        ocr_backend=ocr_backend,
        sample_ocr_interval_seconds=sample_ocr_interval_seconds,
        samples_dir=samples_dir,
    )
    intervals = detect_slide_intervals_from_samples(
        frame_samples=frame_samples,
        duration_seconds=duration,
        slide_change_threshold=slide_change_threshold,
        min_segment_seconds=min_segment_seconds,
        max_segment_seconds=max_segment_seconds,
    )
    intervals = merge_adjacent_visually_similar_intervals(
        cap=cap,
        fps=fps,
        crop_box=crop_box,
        intervals=intervals,
        merge_threshold=duplicate_slide_merge_threshold,
    )
    cues = [
        cue
        for cue in parse_vtt(vtt_path)
        if cue.start_time_seconds <= duration and cue.end_time_seconds >= 0
    ]
    assignments, alignment_warnings = align_cues_to_intervals(
        cues,
        intervals,
        buffer_before_seconds=buffer_before_seconds,
        buffer_after_seconds=buffer_after_seconds,
    )

    artifacts: list[dict[str, Any]] = []
    segments: list[dict[str, Any]] = []
    extra_frame_count = 0
    for interval in intervals:
        segment_cues = assignments.get(interval.segment_id, [])
        transcript_text = " ".join(cue["text"] for cue in segment_cues if cue.get("text")).strip()
        segment_slug = _segment_slug(interval, transcript_text)
        representative_time = _midpoint(interval.start_time_seconds, interval.end_time_seconds)
        representative_artifact = _capture_artifact(
            cap=cap,
            fps=fps,
            crop_box=crop_box,
            images_dir=images_dir,
            source_id=source_id,
            source_title=source_title,
            source_version=source_version,
            ingestion_batch_id=ingestion_batch_id,
            segment_id=interval.segment_id,
            segment_slug=segment_slug,
            timestamp_seconds=representative_time,
            artifact_kind="primary",
            ocr_text=interval.ocr_text,
            ocr_confidence=interval.ocr_confidence,
            ocr_provenance=interval.ocr_provenance,
            detected_title=interval.detected_title,
        )
        artifacts.append(representative_artifact)
        extra_artifacts = _capture_extra_frame_artifacts(
            cap=cap,
            fps=fps,
            crop_box=crop_box,
            images_dir=images_dir,
            source_id=source_id,
            source_title=source_title,
            source_version=source_version,
            ingestion_batch_id=ingestion_batch_id,
            interval=interval,
            segment_slug=segment_slug,
            representative_timestamp=representative_time,
            threshold=extra_frame_threshold,
            max_extra_frames=max_extra_frames_per_segment,
            sampling_interval_seconds=max(sampling_interval_seconds, 1.0),
        )
        artifacts.extend(extra_artifacts)
        extra_frame_count += len(extra_artifacts)
        artifact_ids = [representative_artifact["artifact_id"]] + [artifact["artifact_id"] for artifact in extra_artifacts]
        segments.append(
            {
                "segment_id": interval.segment_id,
                "unit_type": "training_video_slide_segment",
                "source_id": source_id,
                "source_type": "training_video",
                "source_title": source_title,
                "source_version": source_version,
                "ingestion_batch_id": ingestion_batch_id,
                "title": _segment_title(interval, transcript_text),
                "start_time_seconds": round(interval.start_time_seconds, 3),
                "end_time_seconds": round(interval.end_time_seconds, 3),
                "start_timecode": interval.start_timecode,
                "end_timecode": interval.end_timecode,
                "representative_artifact_id": representative_artifact["artifact_id"],
                "artifact_ids": artifact_ids,
                "transcript_cues": segment_cues,
                "transcript_text": transcript_text,
                "ocr_text": "",
                "ocr_confidence": interval.ocr_confidence,
                "ocr_provenance": interval.ocr_provenance,
                "ocr_text_hash": interval.ocr_text_hash,
                "detected_title": interval.detected_title,
                "ocr_text": interval.ocr_text,
                "combined_text": "\n".join(part for part in [transcript_text, interval.ocr_text] if part).strip(),
                "source_refs": [
                    _video_source_ref(
                        source_id,
                        ingestion_batch_id,
                        interval.start_time_seconds,
                        interval.end_time_seconds,
                        segment_id=interval.segment_id,
                    )
                ],
                "confidence": interval.confidence,
                "detection_method": interval.detection_method,
                "segmentation_reasons": interval.segmentation_reasons,
                "warnings": interval.warnings,
                "validation_status": "needs_sme_review",
            }
        )

    quality_report = build_segmentation_quality_report(intervals, assignments, max_segment_seconds)
    report = _build_report(
        video_path=video_path,
        vtt_path=vtt_path,
        source_id=source_id,
        source_title=source_title,
        source_version=source_version,
        ingestion_batch_id=ingestion_batch_id,
        crop_box=crop_box,
        sampling_interval_seconds=sampling_interval_seconds,
        slide_change_threshold=slide_change_threshold,
        intervals=intervals,
        artifacts=artifacts,
        cues=cues,
        assignments=assignments,
        alignment_warnings=alignment_warnings,
        extra_frame_count=extra_frame_count,
        video_metadata={"width": width, "height": height, "fps": fps, "frame_count": frame_count, "duration_seconds": duration},
        ocr_backend=ocr_backend,
        sample_ocr_interval_seconds=sample_ocr_interval_seconds,
        quality_report=quality_report,
    )
    if write_segmentation_inspection:
        write_json(output_path / "candidate_cuts.json", build_candidate_cuts(intervals))
        write_json(output_path / "segmentation_quality_report.json", quality_report)
        write_segmentation_contact_sheet(cap, fps, crop_box, intervals, output_path / "segmentation_contact_sheet.jpg")
    if fail_on_low_quality_segmentation and quality_report["low_quality"]:
        report["errors"].append("Segmentation quality gates failed.")

    validation_errors = validate_training_video_outputs(segments, artifacts, ocr_enabled=ocr_backend != "none")
    report["validation_errors"] = validation_errors
    if validation_errors:
        report["warnings"].append("Validation errors were found in training video outputs.")

    write_json(output_path / "source_artifacts.json", artifacts)
    write_json(output_path / "training_video_slide_segments.json", segments)
    write_json(output_path / "training_video_ingestion_report.json", report)
    cap.release()
    if fail_on_low_quality_segmentation and quality_report["low_quality"]:
        raise RuntimeError("Segmentation quality gates failed. Review training_video_ingestion_report.json.")
    return artifacts, segments, report


def detect_slide_intervals(
    cap: Any,
    duration_seconds: float,
    fps: float,
    crop_box: CropBox,
    sampling_interval_seconds: float,
    slide_change_threshold: float,
    min_segment_seconds: float,
) -> list[SlideInterval]:
    cv2 = _load_cv2()
    previous = None
    current_start = 0.0
    intervals: list[SlideInterval] = []
    pending_warnings: list[str] = []
    sec = 0.0
    while sec <= duration_seconds:
        frame = _read_frame_at(cap, fps, sec)
        if frame is None:
            sec += sampling_interval_seconds
            continue
        small = _small_gray_crop(cv2, frame, crop_box)
        if previous is not None:
            diff = _mean_abs_diff(cv2, previous, small)
            if diff >= slide_change_threshold:
                if sec - current_start >= min_segment_seconds:
                    intervals.append(
                        SlideInterval(
                            index=len(intervals) + 1,
                            start_time_seconds=current_start,
                            end_time_seconds=sec,
                            confidence=_confidence_for_diff(diff, slide_change_threshold),
                            warnings=pending_warnings,
                        )
                    )
                    current_start = sec
                    pending_warnings = []
                else:
                    pending_warnings.append(
                        f"Ignored potential slide change at {format_timecode(sec)} because the segment would be shorter than {min_segment_seconds} seconds."
                    )
        previous = small
        sec += sampling_interval_seconds
    if duration_seconds > current_start:
        intervals.append(
            SlideInterval(
                index=len(intervals) + 1,
                start_time_seconds=current_start,
                end_time_seconds=duration_seconds,
                confidence="medium",
                warnings=pending_warnings,
            )
        )
    return intervals


def collect_frame_samples(
    cap: Any,
    duration_seconds: float,
    fps: float,
    crop_box: CropBox,
    sampling_interval_seconds: float,
    slide_change_threshold: float,
    ocr_client: TesseractOCRClient | None,
    ocr_backend: str,
    sample_ocr_interval_seconds: float,
    samples_dir: Path,
) -> list[FrameSample]:
    cv2 = _load_cv2()
    samples_dir.mkdir(parents=True, exist_ok=True)
    samples: list[FrameSample] = []
    previous_small = None
    last_cut_small = None
    next_ocr_time = 0.0
    sec = 0.0
    while sec <= duration_seconds:
        frame = _read_frame_at(cap, fps, sec)
        if frame is None:
            sec += sampling_interval_seconds
            continue
        small = _small_gray_crop(cv2, frame, crop_box)
        diff_previous = _mean_abs_diff(cv2, previous_small, small) if previous_small is not None else None
        diff_last_cut = _mean_abs_diff(cv2, last_cut_small, small) if last_cut_small is not None else None

        ocr_result = OCRResult("", None, None, None)
        if ocr_client and sec + 0.001 >= next_ocr_time:
            sample_image = samples_dir / f"sample_{slugify(format_timecode(sec))}.jpg"
            _write_crop_image(frame, crop_box, sample_image)
            ocr_result = ocr_client.extract(sample_image)
            provenance = dict(ocr_result.provenance or {})
            provenance["timestamp_seconds"] = round(sec, 3)
            provenance["timestamp_timecode"] = format_timecode(sec)
            ocr_result = OCRResult(
                text=ocr_result.text,
                confidence=ocr_result.confidence,
                backend=ocr_result.backend,
                provenance=provenance,
            )
            next_ocr_time = sec + sample_ocr_interval_seconds

        sample = FrameSample(
            timestamp_seconds=sec,
            timestamp_timecode=format_timecode(sec),
            diff_from_previous=diff_previous,
            diff_from_last_cut=diff_last_cut,
            ocr_text=ocr_result.text,
            ocr_confidence=ocr_result.confidence,
            ocr_text_hash=ocr_text_hash(ocr_result.text),
            detected_title=detect_title_from_ocr(ocr_result.text),
            ocr_provenance=ocr_result.provenance,
        )
        samples.append(sample)
        if last_cut_small is None or (diff_last_cut is not None and diff_last_cut >= slide_change_threshold):
            last_cut_small = small
        previous_small = small
        sec += sampling_interval_seconds
    return samples


def detect_slide_intervals_from_samples(
    frame_samples: list[FrameSample],
    duration_seconds: float,
    slide_change_threshold: float,
    min_segment_seconds: float,
    max_segment_seconds: float,
    ocr_visual_support_ratio: float = 0.65,
) -> list[SlideInterval]:
    if not frame_samples:
        return []
    cuts = [frame_samples[0].timestamp_seconds]
    cut_reasons: dict[float, list[str]] = {frame_samples[0].timestamp_seconds: ["video_start"]}
    last_cut_time = frame_samples[0].timestamp_seconds
    last_accepted_ocr = frame_samples[0].ocr_text
    last_accepted_title = frame_samples[0].detected_title
    pending_warnings: list[str] = []

    for sample in frame_samples[1:]:
        reasons: list[str] = []
        if sample.diff_from_previous is not None and sample.diff_from_previous >= slide_change_threshold:
            reasons.append("visual_diff_previous")
        if sample.diff_from_last_cut is not None and sample.diff_from_last_cut >= slide_change_threshold * 1.2:
            reasons.append("visual_diff_last_cut")
        visual_support = max(sample.diff_from_previous or 0.0, sample.diff_from_last_cut or 0.0)
        has_ocr_visual_support = visual_support >= slide_change_threshold * ocr_visual_support_ratio
        if has_ocr_visual_support and sample.ocr_text and last_accepted_ocr and ocr_text_changed(last_accepted_ocr, sample.ocr_text):
            reasons.append("ocr_text_change_with_visual_support")
        if (
            has_ocr_visual_support
            and sample.detected_title
            and last_accepted_title
            and normalize_ocr_text(sample.detected_title) != normalize_ocr_text(last_accepted_title)
        ):
            reasons.append("ocr_title_change_with_visual_support")

        if reasons:
            if sample.timestamp_seconds - last_cut_time >= min_segment_seconds:
                cuts.append(sample.timestamp_seconds)
                cut_reasons[sample.timestamp_seconds] = reasons
                last_cut_time = sample.timestamp_seconds
                if sample.ocr_text:
                    last_accepted_ocr = sample.ocr_text
                if sample.detected_title:
                    last_accepted_title = sample.detected_title
                pending_warnings = []
            else:
                pending_warnings.append(
                    f"Ignored potential slide change at {sample.timestamp_timecode} because the segment would be shorter than {min_segment_seconds} seconds."
                )

    if cuts[-1] < duration_seconds:
        cuts.append(duration_seconds)
        cut_reasons[duration_seconds] = ["video_end"]

    intervals: list[SlideInterval] = []
    for index, start in enumerate(cuts[:-1], start=1):
        end = cuts[index]
        segment_samples = [sample for sample in frame_samples if start <= sample.timestamp_seconds < end]
        best_ocr = _best_ocr_sample(segment_samples)
        reasons = cut_reasons.get(start, [])
        interval = SlideInterval(
            index=index,
            start_time_seconds=start,
            end_time_seconds=end,
            confidence=_interval_confidence(reasons, best_ocr),
            detection_method="cropped_frame_similarity+ocr" if any("ocr" in reason for reason in reasons) else "cropped_frame_similarity",
            warnings=list(pending_warnings),
            segmentation_reasons=reasons,
            ocr_text=best_ocr.ocr_text if best_ocr else "",
            ocr_confidence=best_ocr.ocr_confidence if best_ocr else None,
            ocr_provenance=best_ocr.ocr_provenance if best_ocr else None,
            ocr_text_hash=best_ocr.ocr_text_hash if best_ocr else None,
            detected_title=best_ocr.detected_title if best_ocr else None,
        )
        if end - start > max_segment_seconds:
            interval.warnings.append(
                f"Segment exceeds max_segment_seconds={max_segment_seconds}; not force-split because visual/OCR evidence did not show a reliable cut."
            )
        intervals.append(interval)
    return intervals


def merge_adjacent_visually_similar_intervals(
    cap: Any,
    fps: float,
    crop_box: CropBox,
    intervals: list[SlideInterval],
    merge_threshold: float = 3.0,
) -> list[SlideInterval]:
    if not intervals:
        return []
    cv2 = _load_cv2()
    merged: list[SlideInterval] = []
    current = intervals[0]
    for candidate in intervals[1:]:
        current_frame = _read_frame_at(cap, fps, _midpoint(current.start_time_seconds, current.end_time_seconds))
        candidate_frame = _read_frame_at(cap, fps, _midpoint(candidate.start_time_seconds, candidate.end_time_seconds))
        diff = None
        if current_frame is not None and candidate_frame is not None:
            diff = _mean_abs_diff(
                cv2,
                _small_gray_crop(cv2, current_frame, crop_box),
                _small_gray_crop(cv2, candidate_frame, crop_box),
            )
        if diff is not None and diff <= merge_threshold:
            current = SlideInterval(
                index=current.index,
                start_time_seconds=current.start_time_seconds,
                end_time_seconds=candidate.end_time_seconds,
                confidence=current.confidence if current.confidence == candidate.confidence else "medium",
                detection_method=current.detection_method,
                warnings=current.warnings + candidate.warnings + [f"Merged adjacent visually similar interval; midpoint diff={diff:.3f}."],
                segmentation_reasons=current.segmentation_reasons + candidate.segmentation_reasons + ["merged_adjacent_visual_duplicate"],
                ocr_text=current.ocr_text or candidate.ocr_text,
                ocr_confidence=current.ocr_confidence if current.ocr_confidence is not None else candidate.ocr_confidence,
                ocr_provenance=current.ocr_provenance or candidate.ocr_provenance,
                ocr_text_hash=current.ocr_text_hash or candidate.ocr_text_hash,
                detected_title=current.detected_title or candidate.detected_title,
            )
        else:
            merged.append(current)
            current = candidate
    merged.append(current)
    for index, interval in enumerate(merged, start=1):
        interval.index = index
    return merged


def _best_ocr_sample(samples: list[FrameSample]) -> FrameSample | None:
    with_text = [sample for sample in samples if sample.ocr_text.strip()]
    if not with_text:
        return None
    return sorted(with_text, key=lambda sample: (sample.ocr_confidence or 0, len(sample.ocr_text)), reverse=True)[0]


def _interval_confidence(reasons: list[str], best_ocr: FrameSample | None) -> str:
    if any(reason in reasons for reason in ("ocr_text_change_with_visual_support", "ocr_title_change_with_visual_support")) and best_ocr:
        return "high"
    if any(reason.startswith("visual_diff") for reason in reasons):
        return "high"
    return "medium"


def validate_training_video_outputs(
    segments: list[dict[str, Any]],
    artifacts: list[dict[str, Any]],
    ocr_enabled: bool = False,
) -> list[str]:
    errors: list[str] = []
    artifact_ids = {artifact.get("artifact_id") for artifact in artifacts}
    for artifact in artifacts:
        for field_name in ("source_id", "source_type", "ingestion_batch_id", "source_refs"):
            if not artifact.get(field_name):
                errors.append(f"Artifact {artifact.get('artifact_id')} missing {field_name}.")
        if artifact.get("linked_context_ids") != []:
            errors.append(f"Artifact {artifact.get('artifact_id')} has linked_context_ids before linking.")
        if artifact.get("linked_runbook_ids") != []:
            errors.append(f"Artifact {artifact.get('artifact_id')} has linked_runbook_ids before linking.")
        if artifact.get("ocr_text") and not ocr_enabled:
            errors.append(f"Artifact {artifact.get('artifact_id')} has OCR text even though OCR is disabled.")
        if artifact.get("ocr_provenance") is not None and not ocr_enabled:
            errors.append(f"Artifact {artifact.get('artifact_id')} has OCR provenance even though OCR is disabled.")
    for segment in segments:
        for field_name in ("source_id", "source_type", "ingestion_batch_id", "source_refs"):
            if not segment.get(field_name):
                errors.append(f"Segment {segment.get('segment_id')} missing {field_name}.")
        representative = segment.get("representative_artifact_id")
        if representative not in artifact_ids:
            errors.append(f"Segment {segment.get('segment_id')} representative artifact does not exist: {representative}")
        for artifact_id in segment.get("artifact_ids", []):
            if artifact_id not in artifact_ids:
                errors.append(f"Segment {segment.get('segment_id')} references missing artifact: {artifact_id}")
        for cue in segment.get("transcript_cues", []):
            if cue.get("alignment_type") not in {"exact_overlap", "buffered_overlap", "nearest_slide"}:
                errors.append(f"Segment {segment.get('segment_id')} has invalid cue alignment_type.")
    return errors


def _clean_vtt_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def _overlap_seconds(start_a: float, end_a: float, start_b: float, end_b: float) -> float:
    return max(0.0, min(end_a, end_b) - max(start_a, start_b))


def _distance_to_interval(cue: TranscriptCue, interval: SlideInterval) -> float:
    if cue.end_time_seconds < interval.start_time_seconds:
        return interval.start_time_seconds - cue.end_time_seconds
    if cue.start_time_seconds > interval.end_time_seconds:
        return cue.start_time_seconds - interval.end_time_seconds
    return 0.0


def _select_best_alignment(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return sorted(
        candidates,
        key=lambda item: (
            -item["overlap_seconds"],
            -item["buffered_overlap_seconds"],
            item["interval"].start_time_seconds,
        ),
    )[0]


def _aligned_cue_record(cue: TranscriptCue, selected: dict[str, Any]) -> dict[str, Any]:
    return {
        "cue_id": cue.cue_id,
        "start_time_seconds": round(cue.start_time_seconds, 3),
        "end_time_seconds": round(cue.end_time_seconds, 3),
        "start_timecode": cue.start_timecode,
        "end_timecode": cue.end_timecode,
        "text": cue.text,
        "alignment_type": selected["alignment_type"],
        "overlap_seconds": round(selected["overlap_seconds"], 3),
        "buffered_overlap_seconds": round(selected["buffered_overlap_seconds"], 3),
        "alignment_confidence": selected["alignment_confidence"],
    }


def _load_cv2() -> Any:
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("OpenCV is required for training video ingestion. Install opencv-python.") from exc
    return cv2


def _build_ocr_client(ocr_backend: str, tesseract_command: str | None) -> TesseractOCRClient | None:
    backend = (ocr_backend or "none").strip().lower()
    if backend == "none":
        return None
    if backend == "tesseract":
        return TesseractOCRClient(command=tesseract_command)
    raise ValueError("Unsupported OCR backend. Use 'none' or 'tesseract'.")


def _validate_crop_box(crop_box: CropBox, width: int, height: int) -> None:
    if crop_box.left < 0 or crop_box.top < 0 or crop_box.right > width or crop_box.bottom > height:
        raise ValueError(f"Crop box {crop_box.as_dict()} is outside video dimensions {width}x{height}.")


def _read_frame_at(cap: Any, fps: float, seconds: float) -> Any | None:
    cap.set(_load_cv2().CAP_PROP_POS_FRAMES, int(seconds * fps))
    ok, frame = cap.read()
    return frame if ok else None


def _write_crop_image(frame: Any, crop_box: CropBox, output_path: Path) -> None:
    cv2 = _load_cv2()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    crop = frame[crop_box.top : crop_box.bottom, crop_box.left : crop_box.right]
    cv2.imwrite(str(output_path), crop, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def _small_gray_crop(cv2: Any, frame: Any, crop_box: CropBox) -> Any:
    crop = frame[crop_box.top : crop_box.bottom, crop_box.left : crop_box.right]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, (160, 90), interpolation=cv2.INTER_AREA)


def _mean_abs_diff(cv2: Any, first: Any, second: Any) -> float:
    return float(cv2.absdiff(first, second).mean())


def _confidence_for_diff(diff: float, threshold: float) -> str:
    if diff >= threshold * 1.5:
        return "high"
    if diff >= threshold:
        return "medium"
    return "low"


def _capture_artifact(
    cap: Any,
    fps: float,
    crop_box: CropBox,
    images_dir: Path,
    source_id: str,
    source_title: str,
    source_version: str | None,
    ingestion_batch_id: str,
    segment_id: str,
    segment_slug: str,
    timestamp_seconds: float,
    artifact_kind: str,
    ocr_text: str = "",
    ocr_confidence: float | None = None,
    ocr_provenance: dict[str, Any] | None = None,
    detected_title: str | None = None,
) -> dict[str, Any]:
    cv2 = _load_cv2()
    frame = _read_frame_at(cap, fps, timestamp_seconds)
    if frame is None:
        raise ValueError(f"Could not capture frame at {format_timecode(timestamp_seconds)}.")
    crop = frame[crop_box.top : crop_box.bottom, crop_box.left : crop_box.right]
    artifact_type = "training_video_slide_frame" if artifact_kind == "primary" else "training_video_extra_frame"
    artifact_id = f"artifact_training_video_{slugify(source_id)}_{segment_slug}_{artifact_kind}_{slugify(format_timecode(timestamp_seconds))}"
    file_name = f"{artifact_id}.jpg"
    storage_path = images_dir / file_name
    cv2.imwrite(str(storage_path), crop, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    title = f"Training Video Segment {format_timecode(timestamp_seconds)}"
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "image_type": "training_video_frame",
        "source_id": source_id,
        "source_type": "training_video",
        "source_title": source_title,
        "source_version": source_version,
        "ingestion_batch_id": ingestion_batch_id,
        "segment_id": segment_id,
        "timestamp_seconds": round(timestamp_seconds, 3),
        "timestamp_timecode": format_timecode(timestamp_seconds),
        "storage_path": str(storage_path),
        "file_name": file_name,
        "file_format": "jpg",
        "title": detected_title or title,
        "short_description": "Captured training video slide frame.",
        "summary": "This artifact captures the visible shared-slide region from the training video.",
        "retrieval_text": f"Training video slide frame captured at {format_timecode(timestamp_seconds)}.",
        "what_to_look_at": [],
        "ocr_text": ocr_text,
        "ocr_confidence": ocr_confidence,
        "ocr_provenance": ocr_provenance,
        "ocr_text_hash": ocr_text_hash(ocr_text),
        "detected_title": detected_title,
        "source_refs": [
            _video_source_ref(source_id, ingestion_batch_id, timestamp_seconds, timestamp_seconds, artifact_id=artifact_id, segment_id=segment_id)
        ],
        "linked_context_ids": [],
        "linked_runbook_ids": [],
        "validation_status": "needs_sme_review",
        "extraction_metadata": {
            "capture_kind": artifact_kind,
            "crop_box": crop_box.as_dict(),
            "ocr_enabled": bool(ocr_text or ocr_provenance),
        },
    }


def _capture_extra_frame_artifacts(
    cap: Any,
    fps: float,
    crop_box: CropBox,
    images_dir: Path,
    source_id: str,
    source_title: str,
    source_version: str | None,
    ingestion_batch_id: str,
    interval: SlideInterval,
    segment_slug: str,
    representative_timestamp: float,
    threshold: float,
    max_extra_frames: int,
    sampling_interval_seconds: float,
) -> list[dict[str, Any]]:
    if max_extra_frames <= 0 or interval.end_time_seconds - interval.start_time_seconds <= sampling_interval_seconds:
        return []
    cv2 = _load_cv2()
    representative_frame = _read_frame_at(cap, fps, representative_timestamp)
    if representative_frame is None:
        return []
    representative_small = _small_gray_crop(cv2, representative_frame, crop_box)
    extras: list[dict[str, Any]] = []
    sec = interval.start_time_seconds
    while sec <= interval.end_time_seconds and len(extras) < max_extra_frames:
        if abs(sec - representative_timestamp) < sampling_interval_seconds:
            sec += sampling_interval_seconds
            continue
        frame = _read_frame_at(cap, fps, sec)
        if frame is None:
            sec += sampling_interval_seconds
            continue
        small = _small_gray_crop(cv2, frame, crop_box)
        diff = _mean_abs_diff(cv2, representative_small, small)
        if diff >= threshold:
            extras.append(
                _capture_artifact(
                    cap=cap,
                    fps=fps,
                    crop_box=crop_box,
                    images_dir=images_dir,
                    source_id=source_id,
                    source_title=source_title,
                    source_version=source_version,
                    ingestion_batch_id=ingestion_batch_id,
                    segment_id=interval.segment_id,
                    segment_slug=segment_slug,
                    timestamp_seconds=sec,
                    artifact_kind=f"extra_{len(extras) + 1}",
                )
            )
        sec += sampling_interval_seconds
    return extras


def _video_source_ref(
    source_id: str,
    ingestion_batch_id: str,
    start_seconds: float,
    end_seconds: float,
    artifact_id: str | None = None,
    segment_id: str | None = None,
) -> dict[str, Any]:
    ref = {
        "source_id": source_id,
        "source_type": "training_video",
        "ingestion_batch_id": ingestion_batch_id,
        "timestamp_start": format_timecode(start_seconds),
        "timestamp_end": format_timecode(end_seconds),
        "start_time_seconds": round(start_seconds, 3),
        "end_time_seconds": round(end_seconds, 3),
    }
    if artifact_id:
        ref["artifact_id"] = artifact_id
    if segment_id:
        ref["segment_id"] = segment_id
    return ref


def _segment_slug(interval: SlideInterval, transcript_text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", transcript_text[:80])
    text = "_".join(words[:6]) if words else interval.start_timecode
    return f"{interval.index:04d}_{slugify(text)}"


def _segment_title(interval: SlideInterval, transcript_text: str) -> str:
    if transcript_text:
        first_sentence = re.split(r"(?<=[.!?])\s+", transcript_text.strip())[0]
        return first_sentence[:100]
    return f"Training Video Segment {interval.start_timecode}"


def _midpoint(start: float, end: float) -> float:
    return start + max(0.0, end - start) / 2


def _build_report(
    video_path: Path,
    vtt_path: Path,
    source_id: str,
    source_title: str,
    source_version: str | None,
    ingestion_batch_id: str,
    crop_box: CropBox,
    sampling_interval_seconds: float,
    slide_change_threshold: float,
    intervals: list[SlideInterval],
    artifacts: list[dict[str, Any]],
    cues: list[TranscriptCue],
    assignments: dict[str, list[dict[str, Any]]],
    alignment_warnings: list[dict[str, Any]],
    extra_frame_count: int,
    video_metadata: dict[str, Any],
    ocr_backend: str,
    sample_ocr_interval_seconds: float,
    quality_report: dict[str, Any],
) -> dict[str, Any]:
    aligned_cue_ids = {cue["cue_id"] for aligned in assignments.values() for cue in aligned}
    nearest_count = sum(1 for aligned in assignments.values() for cue in aligned if cue.get("alignment_type") == "nearest_slide")
    low_confidence_alignments = sum(
        1 for aligned in assignments.values() for cue in aligned if cue.get("alignment_confidence") == "low"
    )
    warnings = [warning for warning in alignment_warnings]
    for interval in intervals:
        for warning in interval.warnings:
            warnings.append({"segment_id": interval.segment_id, "warning": warning})
    return {
        "input_video_path": str(video_path),
        "input_vtt_path": str(vtt_path),
        "source_metadata": {
            "source_id": source_id,
            "source_type": "training_video",
            "source_title": source_title,
            "source_version": source_version,
            "ingestion_batch_id": ingestion_batch_id,
        },
        "video_metadata": video_metadata,
        "crop_configuration": crop_box.as_dict(),
        "sampling_interval_seconds": sampling_interval_seconds,
        "slide_change_threshold": slide_change_threshold,
        "sample_ocr_interval_seconds": sample_ocr_interval_seconds,
        "detected_segment_count": len(intervals),
        "source_artifact_count": len(artifacts),
        "extra_frame_artifact_count": extra_frame_count,
        "transcript_cue_count": len(cues),
        "aligned_cue_count": len(aligned_cue_ids),
        "nearest_slide_cue_count": nearest_count,
        "unassigned_cue_count": max(0, len(cues) - len(aligned_cue_ids)),
        "low_confidence_segment_count": sum(1 for interval in intervals if interval.confidence == "low"),
        "low_confidence_alignment_count": low_confidence_alignments,
        "warnings": warnings,
        "errors": [],
        "segmentation_quality": quality_report,
        "ocr_status": {
            "enabled": ocr_backend != "none",
            "backend": None if ocr_backend == "none" else ocr_backend,
            "message": "OCR backend not configured." if ocr_backend == "none" else f"OCR backend: {ocr_backend}",
        },
    }


def build_candidate_cuts(intervals: list[SlideInterval]) -> list[dict[str, Any]]:
    return [
        {
            "segment_id": interval.segment_id,
            "start_time_seconds": round(interval.start_time_seconds, 3),
            "end_time_seconds": round(interval.end_time_seconds, 3),
            "start_timecode": interval.start_timecode,
            "end_timecode": interval.end_timecode,
            "duration_seconds": round(interval.end_time_seconds - interval.start_time_seconds, 3),
            "confidence": interval.confidence,
            "segmentation_reasons": interval.segmentation_reasons,
            "detected_title": interval.detected_title,
            "ocr_text_hash": interval.ocr_text_hash,
            "ocr_confidence": interval.ocr_confidence,
            "warnings": interval.warnings,
        }
        for interval in intervals
    ]


def build_segmentation_quality_report(
    intervals: list[SlideInterval],
    assignments: dict[str, list[dict[str, Any]]],
    max_segment_seconds: float,
    high_cue_density_threshold: int = 80,
) -> dict[str, Any]:
    long_segments = []
    high_cue_density_segments = []
    ocr_change_warnings = []
    for interval in intervals:
        duration = interval.end_time_seconds - interval.start_time_seconds
        cue_count = len(assignments.get(interval.segment_id, []))
        if duration > max_segment_seconds:
            long_segments.append(
                {
                    "segment_id": interval.segment_id,
                    "duration_seconds": round(duration, 3),
                    "start_timecode": interval.start_timecode,
                    "end_timecode": interval.end_timecode,
                }
            )
        if cue_count > high_cue_density_threshold:
            high_cue_density_segments.append(
                {
                    "segment_id": interval.segment_id,
                    "cue_count": cue_count,
                    "start_timecode": interval.start_timecode,
                    "end_timecode": interval.end_timecode,
                }
            )
        if interval.ocr_text and not interval.detected_title:
            ocr_change_warnings.append({"segment_id": interval.segment_id, "warning": "OCR text found but no title detected."})
    low_quality = bool(long_segments or high_cue_density_segments)
    return {
        "low_quality": low_quality,
        "max_segment_seconds": max_segment_seconds,
        "segment_count": len(intervals),
        "long_segment_count": len(long_segments),
        "long_segments": long_segments,
        "high_cue_density_threshold": high_cue_density_threshold,
        "high_cue_density_segment_count": len(high_cue_density_segments),
        "high_cue_density_segments": high_cue_density_segments,
        "ocr_warning_count": len(ocr_change_warnings),
        "ocr_warnings": ocr_change_warnings,
    }


def write_segmentation_contact_sheet(
    cap: Any,
    fps: float,
    crop_box: CropBox,
    intervals: list[SlideInterval],
    output_path: Path,
    thumb_width: int = 320,
    thumb_height: int = 180,
    columns: int = 4,
) -> None:
    cv2 = _load_cv2()
    if not intervals:
        return
    thumbs = []
    for interval in intervals:
        frame = _read_frame_at(cap, fps, _midpoint(interval.start_time_seconds, interval.end_time_seconds))
        if frame is None:
            continue
        crop = frame[crop_box.top : crop_box.bottom, crop_box.left : crop_box.right]
        thumb = cv2.resize(crop, (thumb_width, thumb_height), interpolation=cv2.INTER_AREA)
        label = f"{interval.index:03d} {interval.start_timecode}-{interval.end_timecode}"
        cv2.rectangle(thumb, (0, 0), (thumb_width, 26), (0, 0, 0), -1)
        cv2.putText(thumb, label, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        thumbs.append(thumb)
    if not thumbs:
        return
    rows = (len(thumbs) + columns - 1) // columns
    sheet = cv2.copyMakeBorder(
        cv2.resize(thumbs[0], (thumb_width, thumb_height)),
        0,
        thumb_height * rows - thumb_height,
        0,
        thumb_width * columns - thumb_width,
        cv2.BORDER_CONSTANT,
        value=(240, 240, 240),
    )
    sheet[:] = (240, 240, 240)
    for index, thumb in enumerate(thumbs):
        row = index // columns
        col = index % columns
        y = row * thumb_height
        x = col * thumb_width
        sheet[y : y + thumb_height, x : x + thumb_width] = thumb
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), sheet, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
