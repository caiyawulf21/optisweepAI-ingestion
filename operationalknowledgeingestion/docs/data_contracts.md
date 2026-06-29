# Data Contracts

These records describe the planned local JSON outputs. Full schemas will be added later.

## SourceBundle

Groups one ingestion source and its related files, metadata, extracted text, and generated references.

## SourceArtifact

Represents a useful artifact found in source material, such as an image, table, diagram, section, or figure.

For training videos, source artifacts may represent cropped slide frames or extra key frames captured from meaningful visual changes within a detected slide interval.

## TrainingVideoSlideSegment

Represents one detected training-video slide interval. It links a representative slide-frame artifact, any extra frame artifacts, timestamped VTT transcript cues, and video timestamp source references. These records are source-normalized inputs for downstream operational context extraction and runbook candidate discovery; they are not operational context records or runbook candidates themselves.

Training video slide segments may include local Tesseract OCR text, confidence, detected title, OCR text hash, and OCR provenance. OCR is additive evidence for segmentation and retrieval preparation; it does not replace transcript timestamps or video timestamp source references.

## TrainingVideoPreparedBundle

Represents the compatibility layer between training-video source normalization and the shared extraction stages. Each training video slide segment is represented as a source bundle page and section so existing operational context and runbook candidate extractors can consume it without a separate semantic pipeline. Timestamp source references are preserved on sections and downstream packets.

## ManualReference

Captures stable references back to manual locations so extracted outputs can be traced to source material.

## OperationalContext

Stores retrieval-ready operational facts, diagnostics, explanations, and constraints extracted from source material.

## Runbook

Represents a reusable procedure or troubleshooting workflow drafted from validated operational context.

## EmbeddingRecord

Represents one retrievable knowledge unit prepared for semantic search. It should keep the embedded text, vector, embedding model metadata, source record ID, source record type, source references, and filter metadata needed by the OptiSweep AI troubleshooting app.

## KnowledgeGraphRecord

Represents operational graph nodes and relationships. It should capture entities such as systems, components, alarms, metrics, screens, artifacts, contexts, and procedures, plus auditable edges that explain how those entities relate.

## ExtractionReport

Summarizes an ingestion run, including outputs produced, warnings, validation findings, and review notes.
