#!/usr/bin/env python
"""Assemble data/output SME review + Cosmos publish handoff folders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.runners.assemble_delivery import assemble_delivery_output


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble data/output delivery folders.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = assemble_delivery_output()
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Assembled: {summary['output_root']}")
        print(f"SME review sources: {len(summary['sme_review'])}")
        print(f"Cosmos publish: {summary['cosmos_publish']}")


if __name__ == "__main__":
    main()
