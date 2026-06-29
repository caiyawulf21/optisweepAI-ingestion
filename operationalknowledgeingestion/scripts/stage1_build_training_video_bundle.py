"""Build v1 normalized records from a training video and external VTT transcript."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from optisweep_ingestion.tools.training_video_builder import (
    build_training_video_bundle,
    parse_crop_box,
)
from optisweep_ingestion.stage_paths import stage_dir

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_video: Path = typer.Option(..., "--source-video", exists=True, readable=True),
    transcript_vtt: Path = typer.Option(..., "--transcript-vtt", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    source_id: str | None = typer.Option(None, "--source-id"),
    source_title: str | None = typer.Option(None, "--source-title"),
    source_version: str | None = typer.Option(None, "--source-version"),
    ingestion_batch_id: str | None = typer.Option(None, "--ingestion-batch-id"),
    crop_box: str | None = typer.Option(None, "--crop-box", help="left,top,right,bottom"),
    sampling_interval_seconds: float = typer.Option(1.0, "--sampling-interval-seconds", min=0.25),
    slide_change_threshold: float = typer.Option(18.0, "--slide-change-threshold", min=0.1),
    min_segment_seconds: float = typer.Option(3.0, "--min-segment-seconds", min=0.0),
    buffer_before_seconds: float = typer.Option(1.5, "--buffer-before-seconds", min=0.0),
    buffer_after_seconds: float = typer.Option(3.0, "--buffer-after-seconds", min=0.0),
    extra_frame_threshold: float = typer.Option(8.0, "--extra-frame-threshold", min=0.1),
    max_extra_frames_per_segment: int = typer.Option(0, "--max-extra-frames-per-segment", min=0),
    ocr_backend: str = typer.Option("none", "--ocr-backend", help="none or tesseract"),
    tesseract_command: str | None = typer.Option(None, "--tesseract-command"),
    sample_ocr_interval_seconds: float = typer.Option(3.0, "--sample-ocr-interval-seconds", min=1.0),
    max_segment_seconds: float = typer.Option(120.0, "--max-segment-seconds", min=10.0),
    max_duration_seconds: float | None = typer.Option(None, "--max-duration-seconds", min=1.0),
    duplicate_slide_merge_threshold: float = typer.Option(3.0, "--duplicate-slide-merge-threshold", min=0.0),
    write_segmentation_inspection: bool = typer.Option(False, "--write-segmentation-inspection"),
    fail_on_low_quality_segmentation: bool = typer.Option(False, "--fail-on-low-quality-segmentation"),
) -> None:
    output_dir = stage_dir(output_dir, "1")
    parsed_crop_box = parse_crop_box(crop_box) if crop_box else None
    artifacts, segments, report = build_training_video_bundle(
        source_video=source_video,
        transcript_vtt=transcript_vtt,
        output_dir=output_dir,
        source_id=source_id,
        source_title=source_title,
        source_version=source_version,
        ingestion_batch_id=ingestion_batch_id,
        crop_box=parsed_crop_box,
        sampling_interval_seconds=sampling_interval_seconds,
        slide_change_threshold=slide_change_threshold,
        min_segment_seconds=min_segment_seconds,
        buffer_before_seconds=buffer_before_seconds,
        buffer_after_seconds=buffer_after_seconds,
        extra_frame_threshold=extra_frame_threshold,
        max_extra_frames_per_segment=max_extra_frames_per_segment,
        ocr_backend=ocr_backend,
        tesseract_command=tesseract_command,
        sample_ocr_interval_seconds=sample_ocr_interval_seconds,
        max_segment_seconds=max_segment_seconds,
        max_duration_seconds=max_duration_seconds,
        duplicate_slide_merge_threshold=duplicate_slide_merge_threshold,
        write_segmentation_inspection=write_segmentation_inspection,
        fail_on_low_quality_segmentation=fail_on_low_quality_segmentation,
    )
    typer.echo(f"Source artifacts written:          {output_dir / 'source_artifacts.json'}")
    typer.echo(f"Training segments written:         {output_dir / 'training_video_slide_segments.json'}")
    typer.echo(f"Training ingestion report written: {output_dir / 'training_video_ingestion_report.json'}")
    typer.echo(f"Segments detected:                 {len(segments)}")
    typer.echo(f"Artifacts captured:                {len(artifacts)}")
    typer.echo(f"Transcript cues aligned:           {report['aligned_cue_count']}")
    typer.echo(f"Validation errors:                 {len(report['validation_errors'])}")


if __name__ == "__main__":
    app()
