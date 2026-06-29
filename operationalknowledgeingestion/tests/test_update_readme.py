from pathlib import Path

from operationalknowledgeingestion.scripts.update_readme import refresh_readme, replace_auto_section


def test_replace_auto_section_updates_only_marked_content() -> None:
    readme = "before\n<!-- AUTO:THING_START -->\nold\n<!-- AUTO:THING_END -->\nafter\n"

    updated = replace_auto_section(readme, "THING", "new")

    assert "before" in updated
    assert "new" in updated
    assert "old" not in updated
    assert "after" in updated


def test_refresh_readme_updates_marked_sections(tmp_path: Path) -> None:
    readme_path = tmp_path / "README.md"
    log_path = tmp_path / "development_log.md"
    readme_path.write_text(
        "\n".join(
            [
                "Top",
                "<!-- AUTO:DEVELOPMENT_LOG_START -->",
                "old log",
                "<!-- AUTO:DEVELOPMENT_LOG_END -->",
                "Bottom",
            ]
        ),
        encoding="utf-8",
    )
    log_path.write_text("# Development Log\n\n## Unreleased\n\n### Added\n- Stage 3 enrichment.\n", encoding="utf-8")

    refreshed = refresh_readme(
        readme_path=readme_path,
        auto_sections={
            "DEVELOPMENT_LOG": log_path,
        },
    )

    updated = readme_path.read_text(encoding="utf-8")
    assert refreshed == ["DEVELOPMENT_LOG"]
    assert "old log" not in updated
    assert "Stage 3 enrichment" in updated
