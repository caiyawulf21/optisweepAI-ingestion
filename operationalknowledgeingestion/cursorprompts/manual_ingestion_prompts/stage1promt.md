Complete Stage 1 of the OptiSweep ingestion pipeline: **Source Bundle Builder**.

The overall project prompt/context already exists in the codebase. Do not rewrite the full project plan. Do not implement later stages.

## Goal

Implement a deterministic Stage 1 pipeline that takes a PDF manual and writes a traceable `source_bundle.json`.

This stage should not use an LLM.

It should not extract actual image files yet.

It should not create operational context, runbooks, source artifacts, embeddings, database records, or runtime assistant logic.

## Stage 1 Output

The CLI should produce:

```text
{output_dir}/source_bundle.json
```

Example:

```bash
python scripts/stage1_extract_source_bundle.py \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

## Implement or update these files

```text
src/optisweep_ingestion/schemas/source_bundle.py
src/optisweep_ingestion/tools/pdf_parser.py
src/optisweep_ingestion/tools/source_bundle_builder.py
src/optisweep_ingestion/services/id_generator.py
src/optisweep_ingestion/utils/json_utils.py
scripts/stage1_extract_source_bundle.py
tests/test_source_bundle_builder.py
README.md
```

If the placeholder files already exist, replace placeholders with Stage 1 implementation.

Leave LangGraph files as placeholders unless needed for imports. Do not build the graph yet.

## Schema requirements

Use Pydantic models in:

```text
src/optisweep_ingestion/schemas/source_bundle.py
```

Create these models:

```text
SourceDocument
SourcePage
SourceSection
SourceFigureRef
SourceTableRef
SourceBundle
```

Fields:

```python
SourceDocument:
  source_document_id: str
  title: str | None
  document_type: str | None
  version: str | None
  document_date: str | None
  source_type: str
  source_path: str

SourcePage:
  page_number: int
  text: str
  text_length: int
  section_id: str | None

SourceSection:
  section_id: str
  title: str
  level: int
  page_start: int | None
  page_end: int | None
  parent_section_id: str | None
  text_preview: str | None

SourceFigureRef:
  figure_id: str
  figure_number: str | None
  title: str | None
  page_number: int | None
  section_id: str | None
  caption_text: str | None

SourceTableRef:
  table_id: str
  table_number: str | None
  title: str | None
  page_number: int | None
  section_id: str | None
  caption_text: str | None

SourceBundle:
  source_bundle_id: str
  source_document: SourceDocument
  pages: list[SourcePage]
  sections: list[SourceSection]
  figure_refs: list[SourceFigureRef]
  table_refs: list[SourceTableRef]
  build_metadata: dict
```

Use simple defaults where reasonable, but keep required fields meaningful.

The serialized JSON should look like:

```json
{
  "source_bundle_id": "manual_optisweep_om_v3",
  "source_document": {
    "source_document_id": "manual_optisweep_om_v3",
    "title": "OptiSweep Operation and Maintenance Manual",
    "document_type": "operation_maintenance_manual",
    "version": "3",
    "document_date": "2025-03-09",
    "source_type": "official_manual",
    "source_path": "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf"
  },
  "pages": [],
  "sections": [],
  "figure_refs": [],
  "table_refs": [],
  "build_metadata": {
    "builder": "source_bundle_builder",
    "stage": "stage_1_source_bundle",
    "llm_used": false
  }
}
```

## PDF parser

Implement:

```text
src/optisweep_ingestion/tools/pdf_parser.py
```

Use PyMuPDF / `fitz`.

Behavior:

* Open the PDF.
* Extract PDF metadata.
* Extract text from each page.
* Return page records with 1-based page numbers.
* Do not OCR.
* Do not extract actual images.
* Do not crop figures.
* If `fitz` is not installed, raise a clear error telling the developer to install `pymupdf`.

Keep this parser simple.

## Source bundle builder

Implement:

```text
src/optisweep_ingestion/tools/source_bundle_builder.py
```

Responsibilities:

* Accept PDF path, output dir, optional source bundle ID, optional source document ID.
* Use the PDF parser to extract metadata and page text.
* Create `SourceDocument`.
* Create `SourcePage` records.
* Detect basic section headings.
* Detect figure references.
* Detect table references.
* Assign stable IDs.
* Assign page numbers.
* Attach nearby caption/title text when possible.
* Assign `section_id` to pages based on detected section starts.
* Assign `page_start` and `page_end` to sections.
* Write `source_bundle.json`.

Keep heading detection simple:

* Detect headings that start with numbered patterns like:

  * `4 Controls`
  * `4.1 Human-machine Interfaces (HMI)`
  * `4.1.2.2 VISU_DATA Screen`
  * `5.8.2 Fault Recovery`
* Detect chapter headings like:

  * `Chapter 4 Controls`
  * `Chapter 5 System Operation`
* Do not try to perfectly parse the manual yet.
* Unmatched pages can have `section_id = null`.

Figure detection:

* Detect references like `Figure 4-22` or `Figure 5-1`.
* Stable ID format: `fig_4_22`.

Table detection:

* Detect references like `Table 4-23` or `Table 5-1`.
* Stable ID format: `table_4_23`.

Avoid duplicates by ID.

## ID helpers

Implement:

```text
src/optisweep_ingestion/services/id_generator.py
```

Functions:

* `slugify(text: str) -> str`
* `make_section_id(prefix: str, heading: str) -> str`
* `make_figure_id(figure_number: str) -> str`
* `make_table_id(table_number: str) -> str`
* `make_source_bundle_id(source_path: str) -> str`

Example outputs:

* `slugify("VISU_DATA Screen")` â†’ `visu_data_screen`
* `make_figure_id("Figure 4-22")` â†’ `fig_4_22`
* `make_table_id("Table 4-23")` â†’ `table_4_23`
* `make_section_id("manual", "4.1.2.2 VISU_DATA Screen")` â†’ `manual_4_1_2_2_visu_data_screen`

## JSON utilities

Implement:

```text
src/optisweep_ingestion/utils/json_utils.py
```

Functions:

* `write_json(path: str | Path, data: Any) -> None`
* `read_json(path: str | Path) -> Any`

Requirements:

* Create parent directories automatically.
* Write UTF-8.
* Pretty print with indentation.
* Support Pydantic models by using `model_dump(mode="json")` when available.

## CLI

Implement:

```text
scripts/stage1_extract_source_bundle.py
```

Use Typer.

Options:

* `--source-pdf`
* `--output-dir`
* `--source-bundle-id`
* `--source-document-id`

Behavior:

* Build source bundle.
* Write `{output_dir}/source_bundle.json`.
* Print a concise success message:

  * path written
  * page count
  * section count
  * figure ref count
  * table ref count
  * LLM used: false

## README update

Add/update a short section:

````markdown
## Current Stage: Stage 1 â€” Source Bundle

The current implementation builds a deterministic source bundle from a PDF manual.

Output:

```text
data/output/manual_optisweep_om_v3/stage_1_source_bundle/source_bundle.json
````

Run:

```bash
python scripts/stage1_extract_source_bundle.py \
  --source-pdf "data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf" \
  --output-dir data/output/manual_optisweep_om_v3
```

This stage does not use an LLM and does not extract actual images yet.

````

## Tests

Implement:

```text
tests/test_source_bundle_builder.py
````

Tests should cover:

1. `slugify`
2. figure ID generation
3. table ID generation
4. section ID generation
5. source bundle can be created from fake page text without requiring a real PDF
6. source bundle output includes:

   * `source_bundle_id`
   * `source_document`
   * `pages`
   * `sections`
   * `figure_refs`
   * `table_refs`
   * `build_metadata`
7. `build_metadata["llm_used"] is False`
8. duplicate figure/table refs are deduplicated

For testability, expose a helper in `source_bundle_builder.py` that can build a source bundle from already-extracted fake page records without opening a PDF.

Example helper name:

```python
build_source_bundle_from_pages(...)
```

## Acceptance criteria

Stage 1 is complete when:

* The CLI runs against a local PDF and writes `source_bundle.json`.
* The output includes document metadata, pages, sections, figure refs, table refs, and build metadata.
* No LLM is called.
* No Stage 2+ functionality is implemented.
* Tests pass.
* README explains how to run Stage 1.

Keep the implementation boring, simple, and reliable.

### UPDATE
Tighten Stage 1 source bundle quality before moving to Stage 2.

The current Stage 1 source bundle runs successfully and extracts page text well. Heartbeat content is detectable in the extracted page text, especially:

* Page 52: main heartbeat stats content, including Figure 4-22, Table 4-8, Last/Max/Min, and the â€œlonger than 10 secondsâ€ warning.
* Page 79: heartbeat timeout alarm entries.
* Page 200: commissioning note to check heartbeat on Visu_Data.
* Pages 11 and 14 also mention heartbeat artifacts, but those are front matter list-of-images/list-of-tables pages and should not be treated as canonical figure/table locations.

The goal of this task is to improve Stage 1 source bundle quality, not to build Stage 2.

Do not implement artifact/image extraction.
Do not implement operational context extraction.
Do not implement runbook extraction.
Do not call an LLM.
Do not add database writes.
Do not add LangGraph orchestration yet.

## Problems to fix

### 1. Section detection is too loose

The current heading detector incorrectly treats front matter/prose as sections, such as:

* address/date lines
* intro text like â€œChapter 9 provides information...â€
* general body prose that happens to match loose patterns

This creates bad section spans, including one bad section owning around 150 pages.

Fix heading detection so it is conservative.

### 2. Figure/table canonical refs are using front matter

Figure/table refs are deduplicated by ID, but the first occurrence is often from the List of Images or List of Tables.

Example problem:

* `fig_4_22` is recorded on page 11 instead of actual content page 52.
* `table_4_8` is recorded on page 14 instead of actual content page 52.

Fix figure/table ref extraction so canonical refs prefer real body content pages over front matter list pages.

### 3. Heartbeat page section assignment is wrong

Page 52 contains the real heartbeat stats content, but currently receives the wrong section ID.

Improve section heading detection and page-to-section assignment so page 52 lands under the appropriate body section, likely the Operator Station HMI Data / VISU_DATA area.

## Required implementation changes

Update Stage 1 only, mainly in:

```text
src/optisweep_ingestion/tools/source_bundle_builder.py
tests/test_source_bundle_builder.py
README.md
```

Add helper functions if useful.

## Section heading detection rules

Make section detection conservative.

A valid body section heading should generally match one of these patterns:

```text
Chapter 4 Controls
4 Controls
4.1 Human-machine Interfaces (HMI)
4.1.2 Operator Station HMI Screens
4.1.2.2 VISU_DATA Screen
5.8.2 Fault Recovery
```

Recommended logic:

1. Process page text line by line.
2. Normalize whitespace.
3. Ignore empty lines.
4. Ignore obvious front matter pages when detecting canonical sections, unless the heading is a real chapter/numbered section.
5. Accept `Chapter N Title` only when:

   * line starts with `Chapter`
   * followed by a number
   * followed by a short title
   * line length is reasonable, e.g. less than 100 chars
6. Accept numbered section headings only when:

   * line starts with a section number pattern: `^\d+(\.\d+)*\s+`
   * there is meaningful title text after the number
   * line length is reasonable, e.g. less than 120 chars
   * title does not end like a sentence paragraph
   * title is not just a date, address, copyright, page footer, or prose
7. Reject prose lines that merely mention a chapter, such as:

   * `Chapter 9 provides information...`
   * `This chapter provides...`
   * `Refer to Chapter 5...`
8. Reject front matter metadata lines, such as:

   * company address
   * document revision history rows
   * dates
   * copyright
   * page footers
   * website/email/phone style lines
9. Reject numbered list steps as section headings when likely procedural steps, for example:

   * `1. Navigate to...`
   * `2. Press...`
   * `3. Verify...`

Add a helper like:

```python
def is_likely_section_heading(line: str) -> bool:
    ...
```

Add a helper like:

```python
def detect_sections_from_pages(pages: list[dict]) -> list[SourceSection]:
    ...
```

Keep this deterministic and simple. Do not overfit only to heartbeat.

## Front matter detection

Add simple logic to identify likely front matter/list pages.

A page should be treated as front matter/list page if its text contains headings like:

```text
Table of Contents
List of Images
List of Tables
Version History
Preface
```

or if it is before the first real chapter and mostly contains list/table-of-contents style lines.

Add a helper like:

```python
def is_front_matter_page(page_text: str, page_number: int) -> bool:
    ...
```

This does not need to be perfect. It just needs to stop list-of-images/list-of-tables pages from becoming canonical figure/table locations.

## Figure/table canonical ref logic

Update figure/table extraction so that refs detected on front matter/list pages are stored separately or deprioritized.

Preferred behavior:

1. Extract all figure/table occurrences.
2. Mark each occurrence with:

   * page_number
   * section_id if known
   * is_front_matter
   * caption_text if available
3. When deduplicating canonical figure/table refs:

   * prefer non-front-matter occurrence
   * prefer occurrence with valid section_id
   * prefer occurrence with nearby caption/title text
   * fallback to first occurrence only if no better occurrence exists

You can keep the public schema simple for now, but internally use occurrence records.

Final `figure_refs` and `table_refs` should contain canonical refs only.

Example expected improvement:

```json
{
  "figure_id": "fig_4_22",
  "figure_number": "Figure 4-22",
  "page_number": 52,
  "section_id": "manual_4_1_2_2_visu_data_screen",
  "caption_text": "Figure 4-22 Heartbeat Stats"
}
```

And:

```json
{
  "table_id": "table_4_8",
  "table_number": "Table 4-8",
  "page_number": 52,
  "section_id": "manual_4_1_2_2_visu_data_screen",
  "caption_text": "Table 4-8 Heartbeat Stats"
}
```

If exact title/caption extraction is imperfect, that is okay. Page and section correctness matter more right now.

## Page-to-section assignment

After detecting valid sections:

1. Sort sections by `page_start`.
2. Assign each page to the latest valid section whose `page_start <= page_number`.
3. End each section at the page before the next section starts.
4. Do not allow one bad section to own the entire manual due to bad heading detection.
5. Pages before the first body section can have `section_id = null`.

## Heartbeat quality smoke check

Add a small deterministic quality check or test helper that can run against the built source bundle.

It should check:

1. Page 52 text contains:

   * `Heartbeat Stats`
   * `Last`
   * `Max`
   * `Min`
   * `10 seconds`
2. `fig_4_22` canonical page is not page 11.
3. `fig_4_22` canonical page should be page 52 if detected.
4. `table_4_8` canonical page is not page 14.
5. `table_4_8` canonical page should be page 52 if detected.
6. Page 52 has a non-null section_id.
7. Page 52 section title should include one of:

   * `VISU_DATA`
   * `Data`
   * `Operator Station HMI`

Do not make the whole build fail only because the exact title string is slightly different, but tests should make the desired behavior clear.

## Tests to add/update

Update:

```text
tests/test_source_bundle_builder.py
```

Add tests for:

1. `is_likely_section_heading` accepts:

   * `Chapter 4 Controls`
   * `4.1 Human-machine Interfaces (HMI)`
   * `4.1.2.2 VISU_DATA Screen`
   * `5.8.2 Fault Recovery`

2. `is_likely_section_heading` rejects:

   * `Chapter 9 provides information about maintenance procedures.`
   * `1. Navigate to the system API screen.`
   * `2. Press SYSTEM STARTUP.`
   * address/date/copyright/footer style lines

3. front matter list pages are not used as canonical figure/table refs when a body occurrence exists.

4. canonical figure/table ref selection prefers:

   * non-front-matter page
   * valid section_id
   * caption text

5. section spans do not allow one prose line to own most of the document.

6. fake heartbeat page fixture assigns page 52 to the expected VISU_DATA-style section.

## README update

Update the Stage 1 README notes to say:

```markdown
Stage 1 now includes quality checks for:
- conservative section heading detection
- front matter filtering
- canonical figure/table reference selection
- heartbeat detectability smoke checks
```

## Acceptance criteria

This task is complete when:

* Source bundle generation still works.
* Page text extraction still works.
* Section detection is more conservative.
* Front matter/list pages are not preferred for canonical figure/table refs.
* Heartbeat content remains detectable on page 52.
* `fig_4_22` and `table_4_8` prefer page 52 over front matter pages when present.
* Page 52 receives a reasonable section assignment.
* Tests pass.
* No Stage 2+ functionality is added.

Keep the implementation simple, deterministic, and traceable.


