from pathlib import Path

from optisweep_ingestion.schemas.source_bundle import (
    SourceBundle,
    SourceDocument,
    SourceFigureRef,
    SourceMetadata,
    SourcePage,
    SourceSection,
)
from optisweep_ingestion.services.id_generator import (
    make_artifact_id_from_figure,
    make_artifact_id_from_page_image,
)
from optisweep_ingestion.tools.artifact_extractor import (
    build_artifact_extraction_report,
    build_artifact_from_figure_ref,
    build_skipped_image_summary,
    classify_image_type,
    get_nearby_text,
    priority_artifact_check,
)


def test_artifact_id_from_figure() -> None:
    assert (
        make_artifact_id_from_figure(
            "manual_optisweep_om_v3",
            "manual",
            "Figure 4-22",
            "Operator Station HMI Data Screen-Heartbeat Stats",
        )
        == "artifact_manual_manual_optisweep_om_v3_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats"
    )


def test_artifact_id_from_page_image() -> None:
    assert (
        make_artifact_id_from_page_image("manual_optisweep_om_v3", "manual", 52, 1)
        == "artifact_manual_manual_optisweep_om_v3_page_52_image_1"
    )


def test_deterministic_image_type_classification() -> None:
    assert classify_image_type("Operator Station HMI Data Screen") == "operator_station_screen"
    assert classify_image_type("Hospital HMI Main Menu") == "hospital_station_screen"
    assert classify_image_type("AGV Fault Screen") == "agv_screen"
    assert classify_image_type("Sensor Locations") == "maintenance_diagram"
    assert classify_image_type("Building Overview Screen") == "system_screen"
    assert classify_image_type("Plastic Blocks") == "maintenance_diagram"
    assert classify_image_type("End Stop") == "maintenance_diagram"
    assert classify_image_type("CLINK Controller") == "maintenance_diagram"
    assert classify_image_type("Controller PCA") == "maintenance_diagram"
    assert classify_image_type("Teknic SD Motor") == "maintenance_diagram"
    assert classify_image_type("Timing Belt") == "maintenance_diagram"
    assert classify_image_type("Stacklight") == "photo"
    assert classify_image_type("Get Metrics Pop-Up Screen") == "system_screen"
    assert classify_image_type("ACB API Screen") == "system_screen"
    assert classify_image_type("Z-Axis CLINK Connections") == "maintenance_diagram"
    assert classify_image_type("A-Axis PCA Connections") == "maintenance_diagram"


def test_nearby_text_window_includes_heartbeat_terms() -> None:
    page_text = "Intro " * 200
    page_text += (
        "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats. "
        "The Heartbeat section provides Last, Max, and Min timing values. "
        "A heartbeat signal longer than 10 seconds can cause operation issues. "
    )
    page_text += "Outro " * 200

    nearby = get_nearby_text(page_text, "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats")

    assert "Heartbeat" in nearby
    assert "Last" in nearby
    assert "Max" in nearby
    assert "Min" in nearby
    assert "10 seconds" in nearby


def test_source_artifact_record_from_fake_source_bundle_figure_ref() -> None:
    bundle = _fake_bundle()
    figure_ref = bundle.figure_refs[0]
    page = bundle.pages[0]

    artifact = build_artifact_from_figure_ref(
        bundle=bundle,
        figure_ref=figure_ref,
        page=page,
        storage_path="data/output/manual_optisweep_om_v3/images/artifact_manual_manual_optisweep_om_v3_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.png",
        file_name="artifact_manual_manual_optisweep_om_v3_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.png",
        file_format="png",
        extraction_metadata={"matching_confidence": "high"},
    )

    assert artifact.artifact_id == "artifact_manual_manual_optisweep_om_v3_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats"
    assert artifact.source_id == "manual_optisweep_om_v3"
    assert artifact.source_type == "manual"
    assert artifact.ingestion_batch_id
    assert artifact.figure_id == "fig_4_22"
    assert artifact.page_number == 52
    assert artifact.section_id == "manual_4_1_2_2_visu_data_screen"
    assert artifact.image_type == "operator_station_screen"
    assert "Heartbeat" in artifact.retrieval_text
    assert "10 seconds" in artifact.retrieval_text
    assert artifact.source_refs[0]["figure_id"] == "fig_4_22"


def test_linked_ids_default_to_empty_lists() -> None:
    artifact = build_artifact_from_figure_ref(
        bundle=_fake_bundle(),
        figure_ref=_fake_bundle().figure_refs[0],
        page=_fake_bundle().pages[0],
    )

    assert artifact.linked_context_ids == []
    assert artifact.linked_runbook_ids == []
    assert artifact.linked_procedure_ids == []


def test_extraction_report_includes_heartbeat_artifact_check(tmp_path: Path) -> None:
    bundle = _fake_bundle()
    image_path = tmp_path / "artifact_manual_manual_optisweep_om_v3_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats.png"
    image_path.write_bytes(b"fake image")
    artifact = build_artifact_from_figure_ref(
        bundle=bundle,
        figure_ref=bundle.figure_refs[0],
        page=bundle.pages[0],
        storage_path=str(image_path),
        file_name=image_path.name,
        file_format="png",
    )

    report = build_artifact_extraction_report(
        bundle=bundle,
        pdf_path="manual.pdf",
        total_pdf_pages=200,
        total_embedded_images_found=1,
        total_images_saved=1,
        artifacts=[artifact],
        missing_figure_images=[],
        low_confidence_matches=[],
        skipped_images=[
            {
                "page_number": 1,
                "image_index": 1,
                "width": 575,
                "height": 97,
                "file_size": 21525,
                "reason": "below_min_dimensions",
            }
        ],
    )

    check = report["heartbeat_artifact_check"]
    assert check["artifact_found"] is True
    assert check["page_number"] == 52
    assert check["retrieval_text_contains_heartbeat"] is True
    assert check["retrieval_text_contains_10_seconds"] is True
    assert check["storage_path_exists"] is True
    assert report["priority_artifact_check"]["fig_4_22"]["artifact_found"] is True
    assert report["skipped_image_summary"]["likely_repeated_header_footer"] == 1
    assert "skipped_images" in report["debug"]


def test_low_confidence_artifact_gets_visual_review_flag() -> None:
    artifact = build_artifact_from_figure_ref(
        bundle=_fake_bundle(),
        figure_ref=_fake_bundle().figure_refs[0],
        page=_fake_bundle().pages[0],
        extraction_metadata={
            "matching_confidence": "low",
            "needs_visual_review": True,
        },
    )

    assert artifact.extraction_metadata["needs_visual_review"] is True


def test_skipped_image_summary_groups_review_noise() -> None:
    summary = build_skipped_image_summary(
        [
            {"width": 575, "height": 97, "reason": "below_min_dimensions"},
            {"width": 41, "height": 39, "reason": "below_min_dimensions"},
            {"width": 600, "height": 600, "reason": "below_min_file_size"},
        ]
    )

    assert summary == {
        "below_min_file_size": 1,
        "likely_repeated_header_footer": 1,
        "tiny_icon": 1,
    }


def test_summary_truncates_cleanly() -> None:
    bundle = _fake_bundle()
    long_text = "First sentence is useful. " + ("middle words " * 120) + "Last sentence."
    page = SourcePage(page_number=52, text=long_text, text_length=len(long_text), section_id=bundle.pages[0].section_id)
    artifact = build_artifact_from_figure_ref(bundle, bundle.figure_refs[0], page=page)

    assert len(artifact.summary) <= 851
    assert artifact.summary.endswith(".")
    assert not artifact.summary.endswith("..")


def test_priority_artifact_check_reports_missing_and_found(tmp_path: Path) -> None:
    bundle = _fake_bundle()
    image_path = tmp_path / "artifact.png"
    image_path.write_bytes(b"fake")
    artifact = build_artifact_from_figure_ref(
        bundle,
        bundle.figure_refs[0],
        page=bundle.pages[0],
        storage_path=str(image_path),
        file_name=image_path.name,
        file_format="png",
    )

    checks = priority_artifact_check([artifact])

    assert checks["fig_4_22"]["artifact_found"] is True
    assert checks["fig_4_22"]["storage_path_exists"] is True
    assert checks["fig_5_2"]["artifact_found"] is False


def _fake_bundle() -> SourceBundle:
    section_id = "manual_4_1_2_2_visu_data_screen"
    return SourceBundle(
        source_bundle_id="manual_optisweep_om_v3",
        source_metadata=SourceMetadata(
            source_id="manual_optisweep_om_v3",
            source_type="manual",
            source_title="OptiSweep Operation and Maintenance Manual",
            source_version="3",
            ingestion_batch_id="batch_test",
            source_document_id="optisweep_operation_and_maintenance_manual_final_1",
        ),
        source_document=SourceDocument(
            source_document_id="optisweep_operation_and_maintenance_manual_final_1",
            title="OptiSweep Operation and Maintenance Manual",
            document_type="operation_maintenance_manual",
            version="3",
            document_date="2025-03-09",
            source_type="manual",
            source_path="manual.pdf",
        ),
        pages=[
            SourcePage(
                page_number=52,
                text=(
                    "Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats. "
                    "The Heartbeat section provides statistics for heartbeat signals including "
                    "Last, Max, Min, and Reset. Heartbeat signals longer than 10 seconds can "
                    "cause operation issues."
                ),
                text_length=220,
                section_id=section_id,
            )
        ],
        sections=[
            SourceSection(
                section_id=section_id,
                title="4.1.2.2 VISU_DATA Screen",
                level=4,
                page_start=49,
                page_end=52,
            )
        ],
        figure_refs=[
            SourceFigureRef(
                figure_id="fig_4_22",
                figure_number="Figure 4-22",
                title="Operator Station HMI Data Screen-Heartbeat Stats",
                page_number=52,
                section_id=section_id,
                caption_text="Figure 4-22: Operator Station HMI Data Screen-Heartbeat Stats",
            )
        ],
        table_refs=[],
        build_metadata={"llm_used": False},
    )
