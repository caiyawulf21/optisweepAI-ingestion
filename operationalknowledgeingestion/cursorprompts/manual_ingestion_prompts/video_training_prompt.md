# Video Training Ingestion Prompt

Build a v1 training video ingestion path for OptiSweep source material.

This is a source-normalization stage, not a runbook drafting stage.

The v1 input format is:

```text
training video file + external .vtt transcript file
```

Do not support video-only transcription in v1.
Do not require embedded captions in v1.
Do not create operational context records directly.
Do not create runbook candidates directly.
Do not create canonical runbooks.

The training video builder should emit:

```text
source_artifacts.json
training_video_slide_segments.json
training_video_ingestion_report.json
```

The emitted records must be compatible with the existing Stage 4 operational
context extractor and Stage 5 runbook candidate extractor so the main
orchestrator can run those stages immediately afterward.

## Architecture

Treat the video as the timeline authority.

The transcript does not identify slide changes. Slide intervals must be detected
from the video frames, then VTT transcript cues are aligned to those intervals.

Use this flow:

```text
video file
  -> sample frames
  -> crop known screen-share region
  -> detect slide intervals by frame similarity
  -> capture representative slide artifacts
  -> capture extra key frames when visual content changes within a slide

.vtt transcript
  -> parse cue timestamps and text
  -> align cues to detected slide intervals

video frames + transcript cues
  -> source_artifacts.json
  -> training_video_slide_segments.json
  -> training_video_ingestion_report.json
```

## Source Metadata

Every emitted record must preserve source lineage:

```json
{
  "source_id": "",
  "source_type": "training_video",
  "source_title": "",
  "source_version": "",
  "ingestion_batch_id": "",
  "source_refs": []
}
```

Use `source_type: "training_video"` for the video-derived slide segments and
artifacts.

If a transcript cue is represented as its own source reference, use
`source_type: "training_transcript"` inside that source reference while keeping
the segment record itself under the parent training video source.

## Screen-Share Layout

Assume a known screen-share layout in v1.

Do not implement automatic participant/sidebar/player-control detection yet.
Support a configurable crop box for the slide/screen-share region.

The crop configuration should be explicit and saved in the ingestion report.
The builder should support a default crop configuration, but the report must
make clear which crop was used.

The crop is used for:

- slide-change detection
- representative slide artifact capture
- extra frame capture
- future OCR input

Avoid using the full video frame for slide-change detection because meeting UI,
participant thumbnails, captions, and playback controls can create false visual
changes.

## Slide-Change Detection

Use deterministic frame similarity for v1.

Sample cropped video frames at a configurable interval. Default to sampling
every 1.0 second unless there is a strong reason to use another value.

Detect slide changes by comparing sampled cropped frames.

Each detected slide interval should include:

- segment_id
- start_time_seconds
- end_time_seconds
- start_timecode
- end_timecode
- representative_frame_path
- confidence
- detection_method
- source_refs
- warnings

The detection should be good enough for review, not perfect.

If detection confidence is low, preserve the segment but write a warning in the
ingestion report.

Do not silently discard uncertain intervals.

## Source Artifacts

Capture each detected slide interval as at least one source artifact.

The whole visible slide/screen-share crop should be captured as the primary
artifact for the interval.

Also capture extra frames when meaningful visual content changes within the same
slide interval, for example:

- menus or side panels opening
- UI controls being selected
- callouts appearing
- pointer or highlight changes that materially alter what a reviewer should see
- on-screen operational state changes without a slide transition

Do not over-capture minor cursor movement, video compression noise, participant
UI changes outside the crop, or caption/player-control changes.

Artifact records should include:

```json
{
  "artifact_id": "",
  "artifact_type": "training_video_slide_frame",
  "source_id": "",
  "source_type": "training_video",
  "ingestion_batch_id": "",
  "segment_id": "",
  "timestamp_seconds": 0.0,
  "timestamp_timecode": "00:00:00.000",
  "storage_path": "",
  "file_name": "",
  "title": "",
  "short_description": "",
  "summary": "",
  "retrieval_text": "",
  "what_to_look_at": [],
  "ocr_text": "",
  "ocr_provenance": null,
  "source_refs": [],
  "linked_context_ids": [],
  "linked_runbook_ids": [],
  "validation_status": "needs_sme_review"
}
```

For v1, OCR backend is not selected yet.

Leave `ocr_text` empty when OCR is not run.
Set `ocr_provenance` to null when OCR is not run.
Do not invent slide text from the image.

If a placeholder OCR interface is added, it must preserve OCR provenance and
confidence later. OCR should be additive, not a replacement for transcript text
or other source text.

## VTT Parsing

Parse the external `.vtt` transcript file into cue records.

Preserve original cue timestamps exactly.

Each parsed cue should include:

- cue_id
- start_time_seconds
- end_time_seconds
- start_timecode
- end_timecode
- text
- raw_text when useful

Do not infer slide numbers from transcript text.
Do not use transcript text as the source of slide-change boundaries.

## Transcript Alignment Rule

For each detected slide interval, attach VTT cues whose timestamps overlap the
slide interval.

Also support a configurable alignment buffer:

```text
default buffer before interval start: 1.5 seconds
default buffer after interval end: 3.0 seconds
```

Preserve original cue timestamps.

For each attached cue, include:

```json
{
  "cue_id": "",
  "start_time_seconds": 0.0,
  "end_time_seconds": 0.0,
  "start_timecode": "00:00:00.000",
  "end_timecode": "00:00:00.000",
  "text": "",
  "alignment_type": "exact_overlap",
  "overlap_seconds": 0.0,
  "buffered_overlap_seconds": 0.0,
  "alignment_confidence": "high"
}
```

Allowed `alignment_type` values:

```text
exact_overlap
buffered_overlap
nearest_slide
```

Definitions:

- `exact_overlap`: the cue overlaps the unbuffered slide interval.
- `buffered_overlap`: the cue does not overlap the unbuffered interval, but
  overlaps the buffered interval.
- `nearest_slide`: the cue does not overlap any unbuffered or buffered interval,
  but is assigned to the nearest detected slide interval to avoid losing it.

If a cue qualifies for multiple slide intervals, assign it to the slide interval
with the greatest actual overlap.

If actual overlap is tied or unclear, assign the cue to the earlier slide.

Record a warning only when confidence is low.

Do not duplicate the same cue across multiple slide segments unless explicitly
requested in a future version.

## Training Video Slide Segment Records

Emit normalized records to `training_video_slide_segments.json`.

Each segment should represent a detected slide interval plus aligned transcript
cues and related artifacts.

Example shape:

```json
{
  "segment_id": "segment_training_video_charger_selection_001",
  "unit_type": "training_video_slide_segment",
  "source_id": "",
  "source_type": "training_video",
  "ingestion_batch_id": "",
  "title": "Charger Selection",
  "start_time_seconds": 6538.0,
  "end_time_seconds": 6571.0,
  "start_timecode": "01:48:58.000",
  "end_timecode": "01:49:31.000",
  "representative_artifact_id": "",
  "artifact_ids": [],
  "transcript_cues": [],
  "transcript_text": "",
  "ocr_text": "",
  "combined_text": "",
  "source_refs": [],
  "confidence": "medium",
  "warnings": [],
  "validation_status": "needs_sme_review"
}
```

`combined_text` may combine transcript text and OCR text only when their
provenance remains clear in the record.

If OCR is not available, `combined_text` should be based on transcript text and
artifact metadata only.

The segment format should be easy for Stage 4 operational context extraction and
Stage 5 runbook candidate discovery to consume.

## Source References

Use timestamp-based source references for training video records.

Example:

```json
{
  "source_id": "training_video_optisweep_charger_selection",
  "source_type": "training_video",
  "ingestion_batch_id": "",
  "timestamp_start": "01:48:58.000",
  "timestamp_end": "01:49:31.000",
  "start_time_seconds": 6538.0,
  "end_time_seconds": 6571.0,
  "artifact_id": "",
  "segment_id": ""
}
```

Transcript cue references should preserve the original cue timestamps.

## Ingestion Report

Write `training_video_ingestion_report.json`.

The report should include:

- input video path
- input VTT path
- source metadata
- crop configuration used
- sampling interval
- slide-change threshold
- detected segment count
- source artifact count
- extra frame artifact count
- transcript cue count
- aligned cue count
- nearest-slide cue count
- unassigned cue count, if any
- low-confidence segment count
- low-confidence alignment count
- warnings
- errors
- OCR status

If OCR is not configured, report OCR status as:

```json
{
  "enabled": false,
  "backend": null,
  "message": "OCR backend not configured for v1."
}
```

## Validation Rules

Validate before writing final outputs:

- every segment has source lineage
- every artifact has source lineage
- every artifact referenced by a segment exists
- every representative_artifact_id exists
- every transcript cue assigned to a segment preserves original timestamps
- every cue alignment_type is one of the allowed values
- `linked_context_ids` and `linked_runbook_ids` are empty
- no operational_context records are created
- no runbook_candidates are created
- no canonical runbooks are created
- OCR text is empty if OCR was not run
- OCR provenance is null if OCR was not run

## Non-Goals For V1

Do not implement:

- video-only transcription
- embedded-caption extraction
- automatic meeting-layout detection
- automatic participant/sidebar removal
- canonical runbook drafting
- relationship linking
- Cosmos writes
- vector embedding generation
- knowledge graph generation

## CLI Shape

Prefer a CLI shaped like:

```bash
python scripts/stage1_build_training_video_bundle.py \
  --source-video data/input/videos/example.mp4 \
  --transcript-vtt data/input/videos/example.vtt \
  --output-dir data/output/training_video_example \
  --source-id training_video_example \
  --source-title "OptiSweep Training Video" \
  --crop-box "left,top,right,bottom"
```

The CLI should not run Stage 4 or Stage 5 directly.

The main orchestrator may run Stage 4 and Stage 5 after this builder completes.


