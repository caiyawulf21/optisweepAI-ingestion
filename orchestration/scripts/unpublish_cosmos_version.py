#!/usr/bin/env python
"""Delete Cosmos documents for one or more Stage 11 publish_version_id partitions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared_pipeline_stages.stage_11.cosmos_publisher import delete_publish_versions


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Delete all Cosmos docs for publish_version_id partition(s).",
    )
    parser.add_argument(
        "--publish-version-id",
        action="append",
        required=True,
        help="Publish version to delete. Repeat for multiple versions.",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Optional dataset filter (e.g. playbooks_prompt_a). Repeatable. Default: all containers.",
    )
    args = parser.parse_args()

    result = delete_publish_versions(
        args.publish_version_id,
        datasets=args.dataset,
    )
    print(json.dumps(result, indent=2))
    if result.get("warnings"):
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
