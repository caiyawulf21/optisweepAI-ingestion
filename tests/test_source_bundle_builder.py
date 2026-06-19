from optisweep_ingestion.services.id_generator import (
    make_figure_id,
    make_section_id,
    make_table_id,
    slugify,
)
from optisweep_ingestion.tools.source_bundle_builder import (
    build_quality_report,
    build_source_bundle_from_pages,
    detect_sections_from_pages,
    is_front_matter_page,
    is_likely_section_heading,
)


def test_id_helpers() -> None:
    assert slugify("VISU_DATA Screen") == "visu_data_screen"
    assert make_figure_id("Figure 4-22") == "fig_4_22"
    assert make_table_id("Table 4-23") == "table_4_23"
    assert (
        make_section_id("manual", "4.1.2.2 VISU_DATA Screen")
        == "manual_4_1_2_2_visu_data_screen"
    )


def test_source_bundle_from_fake_pages_deduplicates_refs() -> None:
    pages = [
        {
            "page_number": 1,
            "text": "\n".join(
                [
                    "Chapter 4 Controls",
                    "4.1 Human-machine Interfaces (HMI)",
                    "Figure 4-22 Heartbeat Stats",
                    "Figure 4-22 Heartbeat Stats",
                    "Table 4-23 HMI Fields",
                ]
            ),
        },
        {
            "page_number": 2,
            "text": "\n".join(
                [
                    "5.8.2 Fault Recovery",
                    "Table 4-23 HMI Fields",
                    "Figure 5-1 Startup Screen",
                ]
            ),
        },
    ]

    bundle = build_source_bundle_from_pages(
        pages=pages,
        source_path="data/input/manuals/OptiSweep Operation and Maintenance Manual - Final 1.pdf",
        metadata={"title": "OptiSweep Operation and Maintenance Manual"},
        source_bundle_id="manual_optisweep_om_v3",
    )
    data = bundle.model_dump(mode="json")

    assert set(data) == {
        "source_bundle_id",
        "source_metadata",
        "source_document",
        "pages",
        "sections",
        "figure_refs",
        "table_refs",
        "build_metadata",
    }
    assert data["source_bundle_id"] == "manual_optisweep_om_v3"
    assert data["source_metadata"]["source_id"] == "manual_optisweep_om_v3"
    assert data["source_metadata"]["source_type"] == "manual"
    assert data["build_metadata"]["llm_used"] is False
    assert len(data["pages"]) == 2
    assert len(data["sections"]) >= 2
    assert {ref["figure_id"] for ref in data["figure_refs"]} == {"fig_4_22", "fig_5_1"}
    assert {ref["table_id"] for ref in data["table_refs"]} == {"table_4_23"}


def test_likely_section_heading_accepts_body_headings() -> None:
    assert is_likely_section_heading("Chapter 4 Controls")
    assert is_likely_section_heading("4.1 Human-machine Interfaces (HMI)")
    assert is_likely_section_heading("4.1.2.2 VISU_DATA Screen")
    assert is_likely_section_heading("5.8.2 Fault Recovery")


def test_likely_section_heading_rejects_prose_steps_and_metadata() -> None:
    rejected = [
        "Chapter 9 provides information about maintenance procedures.",
        "1. Navigate to the system API screen.",
        "2. Press SYSTEM STARTUP.",
        "1349 W Peachtree St NW, Ste 1300",
        "09 March, 2025",
        "©2025 Fortna Inc.",
        "1 1/4-7",
        "1 1/2-6",
        "30 Nm",
    ]
    assert all(not is_likely_section_heading(line) for line in rejected)


def test_front_matter_refs_do_not_win_when_body_occurrence_exists() -> None:
    pages = [
        {
            "page_number": 11,
            "text": "\n".join(
                [
                    "List of Images",
                    "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats",
                    "36",
                ]
            ),
        },
        {
            "page_number": 14,
            "text": "\n".join(
                [
                    "List of Tables",
                    "Table 4-8: Operator Station HMI Data Screen-Heartbeat Stats",
                    "36",
                ]
            ),
        },
        {
            "page_number": 49,
            "text": "4.1.2.2: VISU_DATA SCREEN\nFigure 4-20: Operator Station HMI Data Screen",
        },
        {
            "page_number": 52,
            "text": "\n".join(
                [
                    "4.1.2: Operator Station HMI Screens",
                    "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats",
                    "Description",
                    'The "Heartbeat" section provides statistics for heartbeat signals.',
                    "Last: How long, in milliseconds, the most recent signal between the tipper and WCS took.",
                    "Max: How long, in milliseconds, the longest signal between the tipper and WCS took.",
                    "A heartbeat signal longer than 10 seconds can cause operation issues.",
                    "Min: How long, in milliseconds, the shortest signal between the tipper and WCS took.",
                    "Table 4-8: Operator Station HMI Data Screen-Heartbeat Stats",
                ]
            ),
        },
    ]

    bundle = build_source_bundle_from_pages(
        pages=pages,
        source_path="manual.pdf",
        source_bundle_id="manual",
    )
    figures = {ref.figure_id: ref for ref in bundle.figure_refs}
    tables = {ref.table_id: ref for ref in bundle.table_refs}
    page_52 = next(page for page in bundle.pages if page.page_number == 52)
    section = next(section for section in bundle.sections if section.section_id == page_52.section_id)

    assert is_front_matter_page(pages[0]["text"], 11)
    assert figures["fig_4_22"].page_number == 52
    assert tables["table_4_8"].page_number == 52
    assert page_52.section_id is not None
    assert any(term in section.title for term in ["VISU_DATA", "Data", "Operator Station HMI"])


def test_section_spans_reject_prose_that_would_own_document() -> None:
    pages = [
        {"page_number": 1, "text": "Chapter 4 Controls"},
        {"page_number": 2, "text": "Chapter 9 provides information about maintenance procedures."},
        {"page_number": 3, "text": "4.1 Human-machine Interfaces (HMI)"},
        {"page_number": 4, "text": "1. Navigate to the system API screen."},
    ]

    sections = detect_sections_from_pages(pages, "manual")

    assert [section.title for section in sections] == [
        "Chapter 4 Controls",
        "4.1 Human-machine Interfaces (HMI)",
    ]
    assert sections[0].page_end == 2
    assert sections[1].page_end == 4


def test_title_page_metadata_and_quality_report() -> None:
    pages = [
        {
            "page_number": 1,
            "text": "Operation and Maintenance Manual\nOptiSweep Sorter Sweeper\n09 March, 2025\nVersion 3",
        },
        {"page_number": 49, "text": "4.1.2.2: VISU_DATA SCREEN\nFigure 4-20: Data Screen"},
        {
            "page_number": 52,
            "text": "\n".join(
                [
                    "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats",
                    "Heartbeat Stats",
                    "Last Max Min",
                    "10 seconds",
                    "Table 4-8: Operator Station HMI Data Screen-Heartbeat Stats",
                ]
            ),
        },
    ]

    bundle = build_source_bundle_from_pages(
        pages=pages,
        source_path="manual.pdf",
        metadata={"creationDate": "D:20250309144042-05'00'"},
        source_bundle_id="manual",
    )
    report = build_quality_report(bundle)

    assert bundle.source_document.version == "3"
    assert bundle.source_document.document_date == "2025-03-09"
    assert bundle.pages[1].section_ids == ["manual_4_1_2_2_visu_data_screen"]
    assert report["heartbeat_smoke_check"]["passed"] is True
