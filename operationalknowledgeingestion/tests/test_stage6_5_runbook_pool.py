from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from optisweep_ingestion.stage6_5_runbook_pool import PoolBuildConfig, build_runbook_pool


def test_operational_wrapper_builds_from_stage6_finalized_runbooks(tmp_path: Path) -> None:
    source_root = tmp_path / "manual_optisweep_om_v3"
    finalized_dir = source_root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    finalized_dir.mkdir(parents=True)
    (finalized_dir / "candidate_manual_check_alarms.json").write_text(
        """{
  "procedure_id": "proc_check_alarms_v1",
  "candidate_id": "candidate_manual_check_alarms",
  "title": "Check Operator Station Alarms",
  "summary": "Review active operator station alarms.",
  "procedure_type": "diagnostic",
  "role_required": "operator",
  "when_to_use": "Review active operator station alarms.",
  "steps": [{"step_number": 1, "title": "Review", "instruction": "Review alarms."}],
  "source_candidate_ids": ["candidate_manual_check_alarms"],
  "validation_status": "needs_sme_review",
  "metadata": {"merge_status": "source_finalized", "source_id": "manual_optisweep_om_v3", "source_type": "manual"},
  "source_lineage": [{"source_id": "manual_optisweep_om_v3", "source_type": "manual"}]
}""",
        encoding="utf-8",
    )

    result = build_runbook_pool(
        source_roots=[source_root],
        output_dir=tmp_path / "output",
        config=PoolBuildConfig(use_mock_embedder=True),
    )
    assert result.runbook_count == 1
    assert (tmp_path / "output" / "stage_6_5_runbook_pool" / "runbook_pool.json").exists()
