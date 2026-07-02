Complete Stage 2 of the OptiSweep ingestion pipeline: **Source Artifact / Image Extraction**.

The Stage 1 source bundle builder is already implemented and working. It produces:

```text
data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json
```

Stage 2 should use that source bundle plus the original PDF manual to extract image artifacts and create traceable source artifact records.

Do not implement operational context extraction.
Do not implement runbook extraction.
Do not call an LLM yet.
Do not create embeddings.
Do not write to Cosmos, PostgreSQL, Azure AI Search, or any external service.
Do not build the full LangGraph runtime yet.

This stage is still deterministic.

## Goal

Build a deterministic artifact extraction stage that:

1. Reads `source_bundle.json`
2. Reads the original PDF manual
3. Extracts embedded PDF images where possible
4. Creates stable source artifact records for figures/images
5. Links each artifact to page, section, figure ref, and source document
6. Writes image files locally
7. Writes `source_artifacts.json`
8. Writes an artifact extraction report

The output should make later stages easier:

```text
Stage 3 operational context can reference images.
Stage 4 runbooks can reference images.
Final relationship linking can populate linked_context_ids and linked_runbook_ids.
```

Do not populate linked context/runbook IDs yet.

## Important design rule

Images are source evidence, not runbooks and not operational context by themselves.

A source artifact should answer:

```text
What source image/screenshot/figure is this?
Where did it come from?
What page and section does it belong to?
What figure/table/manual reference is it associated with?
What text around it helps retrieval later?
Where is the local extracted image file?
```

It should not decide:

```text
Which runbook uses this?
Which workflow uses this?
Which troubleshooting branch it belongs to?
What issue trigger routes here?
```

Those links are populated later.

## Implement or update these files

```text
src/optisweep_ingestion/schemas/source_artifact.py
src/optisweep_ingestion/stage2_source_artifacts.py
src/optisweep_ingestion/tools/source_bundle_loader.py
src/optisweep_ingestion/services/id_generator.py
src/optisweep_ingestion/utils/json_utils.py
scripts/stage2_extract_source_artifacts.py
tests/test_artifact_extractor.py
README.md
```

If some files do not exist, create them.

Leave existing Stage 1 code working.

## Output files

Stage 2 should write:

```text
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json
data/output/manual_optisweep_om_v3/images/
```

Example image path:

```text
data/output/manual_optisweep_om_v3/images/artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.png
```

## Source artifact schema

Create or update this file:

```text
src/optisweep_ingestion/schemas/source_artifact.py
```

Use Pydantic.

Keep the schema simple.

```python
class SourceArtifact(BaseModel):
    artifact_id: str
    source_document_id: str
    source_bundle_id: str

    artifact_type: str
    image_type: str | None = None

    title: str | None = None
    figure_id: str | None = None
    figure_number: str | None = None
    table_id: str | None = None
    table_number: str | None = None

    page_number: int | None = None
    section_id: str | None = None

    storage_path: str | None = None
    file_name: str | None = None
    file_format: str | None = None

    caption_text: str | None = None
    nearby_text: str | None = None
    retrieval_text: str | None = None
    summary: str | None = None

    linked_context_ids: list[str] = []
    linked_runbook_ids: list[str] = []
    linked_procedure_ids: list[str] = []

    source_refs: list[dict] = []
    extraction_metadata: dict = {}
```

Allowed `artifact_type` values for now:

```text
manual_figure
manual_page_image
manual_table_reference
unknown_image
```

Allowed `image_type` values for now:

```text
hmi_screenshot
rms_screenshot
system_screen
operator_station_screen
hospital_station_screen
agv_screen
diagram
photo
maintenance_diagram
unknown
```

Use simple string validation for now. Do not overbuild enums unless the project already uses enums.

## Artifact ID rules

Artifact IDs must be stable.

If the artifact maps to a figure ref, use the figure number and title:

```text
artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats
```

If no figure ref exists, use page and image index:

```text
artifact_page_52_image_1
```

Add/update ID helper functions in:

```text
src/optisweep_ingestion/services/id_generator.py
```

Functions:

```python
make_artifact_id_from_figure(figure_number: str, title: str | None) -> str
make_artifact_id_from_page_image(page_number: int, image_index: int) -> str
```

## Image extraction behavior

Use PyMuPDF / `fitz`.

Behavior:

1. Open the PDF.
2. For each page, get embedded images using PyMuPDF.
3. Save each extracted image into:

```text
{output_dir}/images/
```

4. Use stable file names.
5. Prefer linking extracted images to `figure_refs` from `source_bundle.json`.
6. If a page has one figure ref and one image, link them.
7. If a page has multiple figure refs and multiple images, match by order on the page.
8. If matching is uncertain, still create an artifact but mark:

```json
"extraction_metadata": {
  "matching_confidence": "low",
  "matching_notes": "Multiple figures/images on page; matched by order."
}
```

9. Do not invent figure refs.
10. Do not block extraction if a figure image cannot be extracted. Record it in the report.

## Important: PDF image extraction may not perfectly map to visual figures

PyMuPDF may extract:

```text
actual figure screenshots
small icons
logos
background fragments
diagram parts
duplicate images
```

So add filtering.

Skip likely non-useful images when:

```text
width < 100 px
height < 100 px
image file size is extremely small
image appears duplicated on many pages
```

Keep the filtering simple and configurable.

Do not try OCR yet.

Do not crop full page screenshots yet unless embedded images are not available.

## Required fallback: page render for figure refs

If a figure ref exists but no useful embedded image is extracted for that figure, create a fallback artifact record with:

```json
"artifact_type": "manual_figure",
"storage_path": null,
"extraction_metadata": {
  "image_extraction_status": "missing_or_not_extracted",
  "fallback_needed": true
}
```

Do not render/crop the page yet unless it is easy and low-risk.

For now, this is enough because Stage 2 should identify missing images instead of pretending the image was extracted.

## Retrieval text and summary rules

For Stage 2, create deterministic retrieval text and summary from available source bundle data.

Do not call LLM.

For each artifact, create retrieval text like:

```text
Figure 4-22: Operator Station HMI Data Screenâ€”Heartbeat Stats. Source: OptiSweep Operation and Maintenance Manual, page 52, section 4.1.2.2 VISU_DATA Screen. Nearby text: The Heartbeat section provides statistics for heartbeat signals including Last, Max, Min, and Reset.
```

Use:

```text
figure/table caption
page number
section title if available
nearby page text window
source document title
```

Keep `summary` longer than the caption but still deterministic. Example:

```text
This manual figure appears in the VISU_DATA Screen section and is associated with the Operator Station HMI Data Screenâ€”Heartbeat Stats. The nearby text explains that the Heartbeat section provides Last, Max, and Min heartbeat timing values between the tipper and WCS, and warns that heartbeat signals longer than 10 seconds can cause operational issues due to mis-synchronization.
```

This is not final LLM enrichment. It is deterministic source-based summary.

## Nearby text extraction

Implement a helper that gets nearby text from the source bundle page.

Simple approach:

```text
Use the full page text.
If longer than 1200 characters, keep a window around the figure caption.
If caption is not found, keep the first 1200 characters of the page text.
```

Normalize whitespace.

## Image type classification

Use deterministic keyword rules only.

Examples:

```text
If title/caption contains "HMI" -> hmi_screenshot
If title/caption contains "RMS" -> rms_screenshot
If title/caption contains "Hospital HMI" -> hospital_station_screen
If title/caption contains "Operator Station HMI" -> operator_station_screen
If title/caption contains "AGV" -> agv_screen
If title/caption contains "Sensor", "Gearbox", "Pneumatic", "Cable", "Tipper Components" -> maintenance_diagram
If title/caption contains "Station" and likely photo -> photo
Else unknown
```

Do not overthink this. It can be improved later.

## Source refs

Every artifact should include a source ref:

```json
{
  "source_document_id": "optisweep_operation_and_maintenance_manual_final_1",
  "source_type": "official_manual",
  "page": 52,
  "section_id": "optisweep_operation_and_maintenance_manual_final_1_4_1_2_2_visu_data_screen",
  "figure_id": "fig_4_22",
  "figure_number": "Figure 4-22",
  "quote_or_summary": "Figure 4-22 appears on page 52 in the VISU_DATA Screen section."
}
```

If no figure ref exists, include page and section only.

## Artifact extraction report

Create:

```text
artifact_extraction_report.json
```

Suggested schema:

```json
{
  "source_bundle_id": "",
  "source_document_id": "",
  "pdf_path": "",
  "total_pdf_pages": 0,
  "total_figure_refs": 0,
  "total_embedded_images_found": 0,
  "total_images_saved": 0,
  "total_artifacts_created": 0,
  "artifacts_with_saved_images": 0,
  "artifacts_missing_images": 0,
  "artifacts_by_image_type": {},
  "missing_figure_images": [],
  "low_confidence_matches": [],
  "skipped_images": [],
  "warnings": []
}
```

The report should clearly show whether important figures were extracted.

## Heartbeat smoke check

Add a deterministic check in the report for the heartbeat figure:

```json
"heartbeat_artifact_check": {
  "figure_id": "fig_4_22",
  "expected_page": 52,
  "artifact_found": true,
  "page_number": 52,
  "section_id": "optisweep_operation_and_maintenance_manual_final_1_4_1_2_2_visu_data_screen",
  "retrieval_text_contains_heartbeat": true,
  "retrieval_text_contains_10_seconds": true,
  "storage_path_exists": true
}
```

If `storage_path_exists` is false because the embedded image did not extract cleanly, do not fail the whole pipeline. Mark it clearly.

## CLI

Create:

```text
scripts/stage2_extract_source_artifacts.py
```

Use Typer.

Options:

```text
--source-bundle
--source-pdf
--output-dir
```

Example:

```bash
python scripts/stage2_extract_source_artifacts.py \
  --source-bundle data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

Print:

```text
Source artifacts written: ...
Artifact report written: ...
Artifacts created: N
Images saved: N
Missing figure images: N
Heartbeat artifact found: true/false
```

## Tests

Create or update:

```text
tests/test_artifact_extractor.py
```

Tests should cover:

1. artifact ID from figure:

   * `Figure 4-22`, `Operator Station HMI Data Screenâ€”Heartbeat Stats`
   * expected: `artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats`

2. artifact ID from page image:

   * page 52 image 1
   * expected: `artifact_page_52_image_1`

3. deterministic image type classification:

   * Operator Station HMI title -> `operator_station_screen` or `hmi_screenshot`
   * Hospital HMI title -> `hospital_station_screen`
   * AGV title -> `agv_screen`
   * Sensor title -> `maintenance_diagram`

4. nearby text window includes heartbeat terms when page text contains:

   * Heartbeat
   * Last
   * Max
   * Min
   * 10 seconds

5. source artifact record can be built from a fake source bundle figure ref.

6. linked IDs default to empty lists:

   * `linked_context_ids`
   * `linked_runbook_ids`
   * `linked_procedure_ids`

7. extraction report includes heartbeat artifact check.

Do not require a real PDF for most unit tests. Keep PDF extraction test optional or integration-style if the test environment has the manual.

## README update

Add/update Stage 2 section:

````markdown
## Current Stage: Stage 2 â€” Source Artifact / Image Extraction

Stage 2 reads the Stage 1 `source_bundle.json` and the original PDF manual, extracts available embedded images, and creates traceable source artifact records.

Outputs:

```text
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/source_artifacts.json
data/output/manual_optisweep_om_v3/stage_2_source_artifacts/artifact_extraction_report.json
data/output/manual_optisweep_om_v3/images/
````

Run:

```bash
python scripts/stage2_extract_source_artifacts.py \
  --source-bundle data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

This stage is deterministic. It does not call an LLM and does not populate linked context or runbook IDs yet.

```

## Acceptance criteria

Stage 2 is complete when:

- The CLI reads `source_bundle.json`.
- The CLI reads the source PDF.
- `source_artifacts.json` is written.
- `artifact_extraction_report.json` is written.
- Images are saved when PyMuPDF can extract them.
- Missing figure images are reported instead of silently ignored.
- `fig_4_22` creates a source artifact on page 52.
- The heartbeat artifact retrieval text includes:
  - Heartbeat
  - Last
  - Max
  - Min
  - 10 seconds
- Linked context/runbook/procedure IDs exist but are empty lists.
- No LLM is called.
- No Stage 3+ functionality is implemented.
- Tests pass.

Keep the implementation simple, deterministic, and traceable.
```


