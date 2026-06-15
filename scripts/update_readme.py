"""Update generated README sections from project docs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
AUTO_SECTIONS = {
    "INGESTION_PLAN": ROOT / "docs" / "ingestion_plan.md",
    "DEVELOPMENT_LOG": ROOT / "docs" / "development_log.md",
}


def replace_auto_section(readme_text: str, section_name: str, section_text: str) -> str:
    """Replace one marked README section while preserving surrounding text."""
    start_marker = f"<!-- AUTO:{section_name}_START -->"
    end_marker = f"<!-- AUTO:{section_name}_END -->"

    before, found_start, remainder = readme_text.partition(start_marker)
    if not found_start:
        raise ValueError(f"Missing start marker: {start_marker}")

    _current, found_end, after = remainder.partition(end_marker)
    if not found_end:
        raise ValueError(f"Missing end marker: {end_marker}")

    replacement = f"{start_marker}\n{section_text.strip()}\n{end_marker}"
    return f"{before}{replacement}{after}"


def main() -> None:
    """Refresh auto-generated README sections from source docs."""
    readme_text = README_PATH.read_text(encoding="utf-8")

    for section_name, source_path in AUTO_SECTIONS.items():
        section_text = source_path.read_text(encoding="utf-8")
        readme_text = replace_auto_section(readme_text, section_name, section_text)

    README_PATH.write_text(readme_text, encoding="utf-8")
    print("README.md updated.")


if __name__ == "__main__":
    main()
