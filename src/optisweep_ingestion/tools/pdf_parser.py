"""Simple PyMuPDF parser for Stage 1 manual ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_pdf(source_pdf: str | Path) -> dict[str, Any]:
    """Extract metadata and page text from a PDF without OCR or image export."""
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PyMuPDF is required to parse PDFs. Install it with: pip install pymupdf"
        ) from exc

    pdf_path = Path(source_pdf)
    with fitz.open(pdf_path) as document:
        metadata = dict(document.metadata or {})
        pages = [
            {"page_number": index + 1, "text": page.get_text("text") or ""}
            for index, page in enumerate(document)
        ]

    return {"metadata": metadata, "pages": pages}
