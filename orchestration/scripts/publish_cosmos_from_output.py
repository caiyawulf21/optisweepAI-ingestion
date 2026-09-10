#!/usr/bin/env python
"""Push the assembled data/output/cosmos_publish bundle to Cosmos DB."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.paths import OUTPUT_COSMOS_PUBLISH
from orchestration.runners.assemble_delivery import publish_cosmos_from_output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload data/output/cosmos_publish to Cosmos DB.",
    )
    parser.add_argument(
        "--cosmos-publish-dir",
        type=Path,
        default=OUTPUT_COSMOS_PUBLISH,
        help="Directory containing publish_bundle/ (default: data/output/cosmos_publish).",
    )
    parser.add_argument(
        "--publish-scope",
        default="all",
        help="Upload scope: all | case:<id> | source:<source_id>.",
    )
    parser.add_argument(
        "--case-id",
        default=None,
        help="Optional case id used when --publish-scope case:auto.",
    )
    args = parser.parse_args()

    uploaded, version_id, warnings, counts = publish_cosmos_from_output(
        args.cosmos_publish_dir,
        publish_scope=args.publish_scope,
        default_case_id=args.case_id,
    )
    print(f"uploaded: {uploaded}")
    print(f"publish_version_id: {version_id or 'n/a'}")
    print(f"publish_scope: {args.publish_scope}")
    print(f"scoped_document_counts: {counts}")
    for warning in warnings:
        print(f"warning: {warning}")
    if not uploaded:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
