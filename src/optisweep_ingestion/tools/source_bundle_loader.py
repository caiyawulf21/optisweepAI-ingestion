"""Load Stage 1 source bundles from local JSON."""

from __future__ import annotations

from pathlib import Path

from optisweep_ingestion.schemas.source_bundle import SourceBundle
from optisweep_ingestion.utils.json_utils import read_json


def load_source_bundle(path: str | Path) -> SourceBundle:
    return SourceBundle.model_validate(read_json(path))
