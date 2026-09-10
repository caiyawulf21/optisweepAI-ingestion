from shared_pipeline_stages.stage_10.rag_retrieval_text import (
    build_operational_context_retrieval_text,
    build_source_artifact_retrieval_text,
)


def test_operational_context_prefers_existing_retrieval_text() -> None:
    text = build_operational_context_retrieval_text(
        {
            "title": "Ignored when retrieval_text exists",
            "summary": "Summary",
            "retrieval_text": "Compact retrieval text for AGV startup readiness.",
        }
    )
    assert text == "Compact retrieval text for AGV startup readiness."


def test_source_artifact_builds_from_summary_when_retrieval_text_missing() -> None:
    text = build_source_artifact_retrieval_text(
        {
            "title": "AGV status screen",
            "summary": "Screenshot of AGV status screen with error codes.",
            "artifact_type": "manual_figure",
        }
    )
    assert "AGV status screen" in text
    assert "error codes" in text
