"""Stage 2 support - local OCR helpers for incident evidence extraction.

Wraps Tesseract OCR and normalization utilities used to produce page OCR,
artifact OCR, confidence metadata, word counts, and stable text hashes.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import subprocess
from typing import Any


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float | None
    backend: str | None
    provenance: dict[str, Any] | None
    word_count: int


class TesseractOCRClient:
    """Small wrapper around Tesseract TSV output with confidence provenance."""

    def __init__(self, command: str | None = None, psm: int = 6) -> None:
        self.command = command or os.getenv("TESSERACT_CMD") or _default_windows_command() or "tesseract"
        self.psm = psm

    def extract(self, image_path: str | Path) -> OCRResult:
        image = Path(image_path)
        command = [self.command, str(image), "stdout", "--psm", str(self.psm), "tsv"]
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=90,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                "Tesseract is not available. Install Tesseract or set TESSERACT_CMD."
            ) from exc
        except subprocess.CalledProcessError as exc:
            details = (exc.stderr or exc.stdout or "").strip()
            raise RuntimeError(f"Tesseract OCR failed: {details}") from exc

        words: list[str] = []
        confidences: list[float] = []
        for line in completed.stdout.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) < 12:
                continue
            text = parts[11].strip()
            if not text:
                continue
            words.append(text)
            try:
                confidence = float(parts[10])
            except ValueError:
                continue
            if confidence >= 0:
                confidences.append(confidence)
        confidence_value = round(sum(confidences) / len(confidences), 2) if confidences else None
        return OCRResult(
            text=normalize_whitespace(" ".join(words)),
            confidence=confidence_value,
            backend="tesseract",
            provenance={
                "backend": "tesseract",
                "command": self.command,
                "psm": self.psm,
                "source_image_path": str(image),
                "confidence": confidence_value,
            },
            word_count=len(words),
        )


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def normalize_ocr_text(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-z0-9\s]+", " ", value)
    return normalize_whitespace(value)


def ocr_text_hash(text: str) -> str | None:
    normalized = normalize_ocr_text(text)
    if not normalized:
        return None
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:16]


def _default_windows_command() -> str | None:
    candidates = [
        Path(os.getenv("LOCALAPPDATA", "")) / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        Path("C:/Program Files/Tesseract-OCR/tesseract.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None
