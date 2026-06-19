# Operational Knowledge Pipeline Architecture Decisions

This document captures architecture decisions and open design direction for the next operational knowledge ingestion pipeline. It is intentionally broader than the current manual-specific stage prompts.

The current OptiSweep ingestion flow is PDF-first and stage-based. The future pipeline should treat PDF parsing, PowerPoint extraction, OCR, and visual artifact handling as source-specific strategies selected by the pipeline, not as hard-coded assumptions.

## Decision: Source Profiling Before Extraction

The pipeline should begin with a source profiling step before committing to an extraction strategy.

The source profiler should identify:

- Source file type, such as PDF, native PPTX, image folder, HTML export, or mixed source package.
- Document shape, such as manual, slide deck, scanned document, illustrated guide, or export bundle.
- Whether the source has selectable text.
- Whether pages or slides contain embedded raster images.
- Whether important visual content appears to be vector drawings, screenshots, scans, or composed slide objects.
- Whether OCR is likely required.
- Whether page rendering should be used as a fallback or as a primary artifact strategy.

This profiling step should produce explicit routing metadata. Later extraction stages should not have to guess whether a source is a manual PDF, slide PDF, scanned PDF, or native presentation.

## Decision: PyMuPDF Is A Tool, Not The Architecture

PyMuPDF is a good backend for PDF-specific operations:

- PDF metadata extraction.
- Page text extraction when text is selectable.
- Embedded image extraction.
- Page rendering for fallback visual artifacts.

However, PyMuPDF should not define the whole ingestion architecture. It should be one adapter used by the pipeline when the source profile says the input is a PDF or PDF-like source.

The future pipeline should route work by source profile:

```text
source intake
  -> source profiling
  -> extraction strategy selection
  -> source-specific extraction
  -> normalized operational knowledge bundle
  -> quality assessment
  -> optional OCR / visual review / human review
```

## Decision: PowerPoint Exported To PDF Is A Slide PDF

A PowerPoint exported to PDF should be treated as a slide-deck PDF, not as a normal manual PDF.

PyMuPDF can still be useful for this source type:

- Each slide becomes a PDF page.
- Visible slide text may be extractable.
- Some embedded images may be extractable.
- Each slide can be rendered as a full-page image.

But slide PDFs carry different risks from manual PDFs:

- PowerPoint shapes, arrows, grouped objects, and diagrams may become vector drawing commands instead of extractable images.
- Slide reading order may be spatial and unreliable.
- Speaker notes are usually lost.
- Animations and stepwise builds are lost.
- Hidden slides may or may not be included depending on export settings.
- Screenshots and diagram labels may still require OCR.

For slide PDFs, the preferred strategy is:

```text
extract selectable text when available
render every slide/page as a visual artifact
extract embedded images when useful
run OCR only when needed and store OCR confidence/provenance
```

This differs from a text-heavy manual PDF, where page rendering can usually be a fallback only when embedded images are missing.

## Decision: OCR Is Additive, Not A Replacement

OCR should be treated as an enrichment layer, not as a replacement for source text.

OCR is useful when:

- The PDF is scanned.
- Screenshots contain important labels or values.
- Diagrams contain text that is not selectable.
- Slide renders contain text that was not captured by PDF text extraction.

OCR output must carry provenance and confidence, including:

- Source page or slide number.
- Source image path or rendered page path.
- OCR engine or model used.
- Confidence score when available.
- Bounding boxes when available.
- Whether the OCR text was used for retrieval, summarization, or candidate extraction.

The pipeline should avoid silently merging OCR text into authoritative source text. Downstream stages need to know whether a claim came from selectable source text, OCR-derived text, visual interpretation, or LLM-generated summarization.

## Target Normalized Source Model

All source-specific extractors should eventually write into a common normalized structure. The exact schema can evolve, but the conceptual model should look like:

```json
{
  "source_kind": "slide_pdf",
  "source_path": "path/to/source.pdf",
  "units": [
    {
      "unit_type": "slide",
      "unit_number": 1,
      "text": "...",
      "rendered_image_path": "...",
      "embedded_artifacts": [],
      "ocr_text": null,
      "confidence": {},
      "provenance": {}
    }
  ]
}
```

For a manual PDF, `unit_type` may be `page`. For native PowerPoint, it may be `slide`. For image folders, it may be `image`. Downstream stages should operate on normalized units instead of directly depending on the original file type.

## Open Questions

- Should the first source profiler be deterministic only, or should it include an LLM-assisted classification pass?
- Should source profiling happen as a new Stage 0, or should it replace part of Stage 1?
- What OCR backend should be preferred for local development versus production?
- Should slide PDFs always render every page, or should the profiler decide based on visual density?
- How should human review be triggered when extraction quality is low?

