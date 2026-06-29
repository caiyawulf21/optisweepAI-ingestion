"""Retry Stage 4 operational context extraction for selected sections."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECT_PARENT = ROOT.parent
SRC = ROOT / "src"
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import typer

from operationalknowledgeingestion.src.optisweep_ingestion.services.source_ref_service import (
    apply_lineage,
    lineage_from_bundle,
)
from operationalknowledgeingestion.src.optisweep_ingestion.tools.operational_context_extractor import (
    AzureOpenAIContextClient,
    build_extraction_report,
    build_source_packets,
    finalize_context_record,
    validate_context_record,
)
from operationalknowledgeingestion.src.optisweep_ingestion.utils.json_utils import read_json, write_json
from optisweep_ingestion.stage_paths import stage_dir

app = typer.Typer(add_completion=False)


@app.command()
def main(
    source_bundle: Path = typer.Option(..., "--source-bundle", exists=True, readable=True),
    source_artifacts: Path = typer.Option(..., "--source-artifacts", exists=True, readable=True),
    existing_context: Path = typer.Option(..., "--existing-context", exists=True, readable=True),
    existing_report: Path = typer.Option(..., "--existing-report", exists=True, readable=True),
    output_dir: Path = typer.Option(..., "--output-dir"),
    section_id: list[str] = typer.Option(..., "--section-id"),
) -> None:
    output_dir = stage_dir(output_dir, "4")
    bundle = read_json(source_bundle)
    artifacts = read_json(source_artifacts)
    contexts = read_json(existing_context)
    prior_report = read_json(existing_report)
    if not isinstance(artifacts, list):
        raise typer.BadParameter("source_artifacts_enriched.json must contain a list.")
    if not isinstance(contexts, list):
        raise typer.BadParameter("operational_context.json must contain a list.")

    target_section_ids = {str(item) for item in section_id}
    lineage = lineage_from_bundle(bundle)
    known_artifact_ids = {a["artifact_id"] for a in artifacts if a.get("artifact_id")}
    packets = [
        packet
        for packet in build_source_packets(bundle, artifacts, lineage)
        if str(packet.get("section_id") or "") in target_section_ids
    ]
    if not packets:
        raise typer.BadParameter("No matching source sections found for supplied --section-id values.")

    client = AzureOpenAIContextClient()
    repaired_contexts: list[dict] = []
    failed_packets: list[dict] = []
    warnings = list(prior_report.get("warnings") or [])

    for packet in packets:
        try:
            raw_records = client.extract(packet)
        except Exception as exc:
            failed_packets.append({"section_id": packet.get("section_id"), "error": str(exc)})
            continue
        for record in raw_records:
            record = apply_lineage(record, lineage)
            record = finalize_context_record(record)
            errors = validate_context_record(record, known_artifact_ids)
            if errors:
                warnings.append(
                    f"Dropped repair record '{record.get('context_id', '?')}' from section "
                    f"'{packet.get('section_id', '?')}': {'; '.join(errors)}"
                )
            else:
                repaired_contexts.append(record)

    merged_by_id: dict[str, dict] = {
        str(context.get("context_id")): dict(context)
        for context in contexts
        if context.get("context_id")
    }
    for context in repaired_contexts:
        merged_by_id[str(context.get("context_id"))] = context
    merged_contexts = list(merged_by_id.values())

    repaired_sections = {
        ref.get("section_id")
        for context in repaired_contexts
        for ref in context.get("source_refs") or []
        if isinstance(ref, dict) and ref.get("section_id")
    }
    remaining_prior_failures = [
        failure
        for failure in prior_report.get("failed_packets") or []
        if str(failure.get("section_id") or "") not in repaired_sections
    ]
    all_failures = [*remaining_prior_failures, *failed_packets]

    report = build_extraction_report(
        source_bundle_path=str(source_bundle),
        source_artifacts_path=str(source_artifacts),
        contexts=merged_contexts,
        lineage=lineage,
        llm_used=True,
        failed_packets=all_failures,
        warnings=warnings,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "operational_context.json", merged_contexts)
    write_json(output_dir / "operational_context_extraction_report.json", report)

    typer.echo(f"Sections retried:          {len(packets)}")
    typer.echo(f"Contexts repaired:         {len(repaired_contexts)}")
    typer.echo(f"Remaining failed packets:  {len(all_failures)}")
    typer.echo(f"Operational context wrote: {output_dir / 'operational_context.json'}")
    typer.echo(f"Report wrote:              {output_dir / 'operational_context_extraction_report.json'}")


if __name__ == "__main__":
    app()
