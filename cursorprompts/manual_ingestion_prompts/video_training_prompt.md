# Refactor Operational Knowledge Extraction Pipeline to Support Multiple Source Types

## Background

The current extraction pipeline was originally designed around a single source type:

* OptiSweep Operation & Maintenance Manual (PDF)

Since then, the architecture has evolved.

The pipeline is no longer intended to be a **manual ingestion pipeline**.

It is now the **Operational Knowledge Extraction Pipeline** for the OptiSweep AI Support Assistant.

The long-term goal is to support multiple operational knowledge sources while sharing one downstream extraction architecture.

Current and planned source types include:

* Operation & Maintenance Manuals (PDF)
* Training Slide Decks (PowerPoint/PDF)
* Training Videos with `.vtt` transcripts
* Incident Records
* SOPs
* SME-authored Documentation
* Future enterprise knowledge sources

Every supported source type should ultimately produce the same normalized intermediate assets:

```text
Source Artifacts
        ↓
Operational Context
        ↓
Runbook Candidates
```

These source-specific outputs later feed into:

```text
Candidate Pool
        ↓
Canonical Runbook Drafting
        ↓
Relationship Linking
        ↓
Validation
```

Canonical runbooks must **never** be generated directly from a single source.

---

# Primary Objective

Refactor the existing manual extraction pipeline into a generalized Operational Knowledge Extraction Pipeline.

Do **not** rewrite the downstream stages.

Instead:

1. Introduce a source detection stage.
2. Introduce source-specific bundle builders.
3. Migrate the existing manual PDF logic into a Manual Bundle Builder.
4. Add a new Training Video Bundle Builder.
5. Keep every downstream stage unchanged.

The goal is to ensure every source type enters the shared pipeline through the same normalized interface.

---

# Desired Architecture

```text
Raw Input
      │
      ▼

Source Detector

      │

      ├───────────────┐
      │               │
      ▼               ▼

Manual Bundle      Video Bundle
Builder            Builder

      │               │
      └──────┬────────┘
             │

      source_bundle.json

             │

      Stage 3
      Source Artifacts

             │

      Stage 4
      Operational Context

             │

      Stage 5
      Runbook Candidates

             │

      Stage 6
      Candidate Pool

             │

      Stage 7
      Canonical Runbooks

             │

      Stage 8
      Relationship Linking

             │

      Stage 9
      Validation
```

The pipeline below `source_bundle.json` should not care where the data originated.

---

# Refactor Existing Structure

Rename concepts where appropriate.

Examples:

```text
manual_ingestion
```

should become

```text
operational_knowledge_extraction
```

Similarly:

```text
manual_ingestion_plan.md
```

should become something similar to

```text
operational_knowledge_pipeline.md
```

Use generalized terminology wherever possible.

Avoid introducing "manual-only" naming into new code.

---

# New Source Detector

Create a source detector responsible for identifying supported input packages.

Supported source types:

```text
manual_pdf

training_slide_deck

training_video_with_vtt

incident_bundle

sop_document

sme_document

unknown
```

The detector should inspect the input directory rather than rely solely on CLI flags.

Example:

```text
input/

    manual.pdf

→ manual_pdf
```

```text
input/

    training.mp4
    training.vtt

→ training_video_with_vtt
```

---

# Source-Specific Bundle Builders

Create bundle builders.

```text
builders/

    manual_bundle_builder.py

    training_video_bundle_builder.py

    slide_bundle_builder.py

    incident_bundle_builder.py
```

Every builder must output the same schema:

```text
source_bundle.json
```

Downstream stages must not require modification when additional builders are added later.

---

# Training Video Builder

Implement a new Training Video Bundle Builder.

The video becomes the timeline authority.

Pipeline:

Video
+
VTT Transcript

↓

Parse transcript

↓

Detect slide intervals

↓

Capture representative slide frames

↓

Crop to presentation area

↓

OCR slides

↓

Align transcript cues to slide intervals

↓

Emit normalized training video segment records

Each segment should contain:

* OCR text
* Transcript text
* Slide timestamps
* Artifact reference
* Source lineage

These segment records become input for the existing Stage 3+ pipeline.

---

# Directory Expectations

Use the existing project structure wherever practical.

Add new folders only where they improve separation of responsibilities.

Prefer introducing:

```text
src/optisweep_ingestion/

    detectors/

    builders/

    stages/
```

rather than creating an entirely separate pipeline.

---

# Important Constraints

Do not break the existing manual extraction pipeline.

The existing manual extraction should continue working using the new Manual Bundle Builder.

Do not rewrite downstream extraction stages unless required.

Maintain backward compatibility where practical.

Preserve source lineage everywhere:

* source_id
* source_type
* ingestion_batch_id
* source_refs

Do not introduce workflow logic, routing logic, trigger conditions, ML labels, or decision-tree behavior into source extraction.

---

# Deliverables

1. Refactored architecture.
2. Source detector.
3. Manual Bundle Builder.
4. Training Video Bundle Builder.
5. Updated CLI entry point.
6. Updated directory structure.
7. Documentation describing how new source types can be added in the future.
