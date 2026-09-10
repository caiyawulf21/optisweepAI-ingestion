#!/usr/bin/env python
"""Run the LangGraph ingestion agent for one uploaded source file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestration.graph.ingestion_graph import run_ingestion


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OptiSweep LangGraph ingestion for one source file.")
    parser.add_argument("--source", type=Path, required=True, help="Path to uploaded PDF or video.")
    parser.add_argument("--companion", type=Path, action="append", default=[], help="Companion file (e.g. .vtt).")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--source-stages", default=None, help="Override source stages, e.g. 1,2,3,4,5,6,8")
    parser.add_argument("--shared-stages", default=None, help="Override shared stages when --with-publish is set.")
    parser.add_argument("--no-llm", action="store_true", help="Disable Azure OpenAI stages (deterministic only).")
    parser.add_argument(
        "--with-publish",
        action="store_true",
        help="Also run shared ingest Stages 6.5-10 after source Stages 1-8.",
    )
    parser.add_argument(
        "--publish-to-cosmos",
        action="store_true",
        help="Build Stage 11 bundle and upload from data/output/cosmos_publish when env is configured.",
    )
    parser.add_argument(
        "--publish-scope",
        default="all",
        help="Cosmos upload scope: all | case:<id> | case:auto | source:<source_id>.",
    )
    parser.add_argument("--ocr-backend", default="azure_cv", choices=["none", "tesseract", "azure_cv"])
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--source-title", default=None)
    parser.add_argument("--source-id", default=None, help="Override the filename-derived source id (operational sources).")
    parser.add_argument("--json", action="store_true", help="Print final state as JSON.")
    args = parser.parse_args()

    result = run_ingestion(
        args.source,
        companion_paths=args.companion,
        output_dir=args.output_dir,
        source_stages=args.source_stages,
        shared_stages=args.shared_stages,
        use_llm=not args.no_llm,
        run_shared_publish=args.with_publish,
        publish_to_cosmos=args.publish_to_cosmos,
        publish_scope=args.publish_scope,
        ocr_backend=args.ocr_backend,
        max_workers=args.max_workers,
        source_title=args.source_title,
        source_id=args.source_id,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"status: {result.get('status')}")
        print(f"source_type: {result.get('source_type')}")
        print(f"output_dir: {result.get('output_dir')}")
        print(f"publish_scope: {result.get('publish_scope')}")
        for message in result.get("messages") or []:
            print(message)
        for error in result.get("errors") or []:
            print(f"ERROR: {error}")

    if result.get("status") != "succeeded":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
