"""All stages docs utility: refresh generated incidence README sections.

This support script is not an ingestion stage. It keeps stage tracker and
development-status documentation synchronized from docs/development_status.md.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
AUTO_SECTIONS = {
    "DEVELOPMENT_STATUS": ROOT / "docs" / "development_status.md",
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


def refresh_readme(
    readme_path: Path = README_PATH,
    auto_sections: Mapping[str, Path] = AUTO_SECTIONS,
) -> list[str]:
    """Refresh generated README sections from source docs."""
    readme_text = readme_path.read_text(encoding="utf-8")
    refreshed: list[str] = []

    for section_name, source_path in auto_sections.items():
        section_text = source_path.read_text(encoding="utf-8")
        readme_text = replace_auto_section(readme_text, section_name, section_text)
        refreshed.append(section_name)

    readme_path.write_text(readme_text, encoding="utf-8")
    return refreshed


def main() -> None:
    refreshed = refresh_readme()
    print("README.md updated: " + ", ".join(refreshed))


if __name__ == "__main__":
    main()
