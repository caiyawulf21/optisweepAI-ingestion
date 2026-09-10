#!/usr/bin/env python
"""Watch data/inbox (and optional SharePoint) and run the LangGraph ingestion agent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.intake import start_watch
from orchestration.intake.sharepoint import ensure_sharepoint_sync_layout, load_sharepoint_config
from orchestration.paths import ensure_inbox_layout


def main() -> None:
    parser = argparse.ArgumentParser(description="Watch data/inbox and ingest uploaded OptiSweep sources.")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Skip shared Stages 6.5-10 (default is to run them after each source).",
    )
    parser.add_argument(
        "--with-publish",
        action="store_true",
        help="Deprecated alias: shared publish is on by default. Use --no-publish to disable.",
    )
    parser.add_argument(
        "--publish-to-cosmos",
        action="store_true",
        help="Also run Stage 11 cumulative Cosmos upload when COSMOS_* env is set.",
    )
    parser.add_argument(
        "--publish-scope",
        default="all",
        help="Cosmos upload scope. Default all (safe for AUTO_PUBLISH_VERSION).",
    )
    parser.add_argument("--source-stages", default=None)
    parser.add_argument("--shared-stages", default=None)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument(
        "--sharepoint-poll-seconds",
        type=float,
        default=30.0,
        help="When SharePoint is configured, poll interval for new remote inbox files.",
    )
    parser.add_argument(
        "--no-sharepoint-review",
        action="store_true",
        help="Do not mirror data/output/sme_review back to SharePoint review/.",
    )
    args = parser.parse_args()

    ensure_inbox_layout()
    sp = load_sharepoint_config()
    if sp.mode == "sync":
        ensure_sharepoint_sync_layout(sp)
        print(f"[inbox] SharePoint sync root: {sp.sync_root}")

    start_watch(
        use_llm=not args.no_llm,
        run_shared_publish=not args.no_publish,
        publish_to_cosmos=args.publish_to_cosmos,
        publish_scope=args.publish_scope,
        source_stages=args.source_stages,
        shared_stages=args.shared_stages,
        max_workers=args.max_workers,
        push_sharepoint_review=not args.no_sharepoint_review,
        poll_sharepoint_seconds=args.sharepoint_poll_seconds,
    )


if __name__ == "__main__":
    main()
