from operationalknowledgeingestion.src.optisweep_ingestion.tools.candidate_pool_builder import build_candidate_pool, cluster_candidates


def test_groups_similar_candidates_and_preserves_lineage(tmp_path) -> None:
    candidates = [
        _candidate(
            candidate_id="manual_candidate_check_heartbeat",
            title="Check Operator Station Heartbeat Stats",
            goal="Verify heartbeat timing between the tipper and WCS.",
            source_type="manual",
            artifact_ids=["artifact_manual_fig_4_22"],
            context_ids=["ctx_manual_operator_station_heartbeat"],
            refs=[{"page": 52, "section_id": "sec_heartbeat"}],
        ),
        _candidate(
            candidate_id="incident_candidate_verify_heartbeat",
            title="Verify Heartbeat Values",
            goal="Check heartbeat values on the operator station during a timeout investigation.",
            source_type="incident",
            artifact_ids=["artifact_incident_229374_screenshot_01"],
            context_ids=["ctx_incident_heartbeat_timeout_pattern"],
            refs=[{"incident_id": "229374"}],
        ),
    ]

    clusters = cluster_candidates(candidates)

    assert len(clusters) == 1
    cluster = clusters[0]
    assert cluster.candidate_count == 2
    assert cluster.source_types == ["manual", "incident"]
    assert cluster.aggregate_artifact_ids == [
        "artifact_manual_fig_4_22",
        "artifact_incident_229374_screenshot_01",
    ]
    packet = cluster.candidate_packets[0]
    assert packet.source_id == "source_manual"
    assert packet.ingestion_batch_id == "batch_test"
    assert packet.source_refs


def test_keeps_distinct_opposing_procedures_separate() -> None:
    clusters = cluster_candidates(
        [
            _candidate("candidate_start_system", "Start OptiSweep System", "Start the OptiSweep system.", "manual"),
            _candidate("candidate_stop_system", "Stop OptiSweep System", "Stop the OptiSweep system.", "manual"),
        ]
    )

    assert len(clusters) == 2
    assert sorted(cluster.normalized_title for cluster in clusters) == ["Start OptiSweep System", "Stop OptiSweep System"]


def test_build_candidate_pool_writes_output(tmp_path) -> None:
    input_path = tmp_path / "runbook_candidates.json"
    input_path.write_text(
        """[
  {
    "candidate_id": "candidate_manual_check_alarms",
    "title": "Check Operator Station Alarms",
    "candidate_goal": "Review active operator station alarms.",
    "likely_procedure_type": "diagnostic",
    "likely_role_required": "operator",
    "summary": "Review alarms.",
    "related_artifact_ids": [],
    "related_context_ids": [],
    "source_refs": [{"page": 10}],
    "evidence_source_refs": [],
    "source_id": "manual_optisweep",
    "source_type": "manual",
    "ingestion_batch_id": "batch_test"
  }
]""",
        encoding="utf-8",
    )

    pool = build_candidate_pool([input_path], tmp_path, generated_at="2026-06-19T00:00:00Z")

    assert pool.candidate_cluster_count == 1
    assert (tmp_path / "candidate_pool.json").exists()
    assert pool.generated_at == "2026-06-19T00:00:00Z"


def _candidate(
    candidate_id: str,
    title: str,
    goal: str,
    source_type: str,
    artifact_ids: list[str] | None = None,
    context_ids: list[str] | None = None,
    refs: list[dict] | None = None,
) -> dict:
    return {
        "candidate_id": candidate_id,
        "title": title,
        "candidate_goal": goal,
        "likely_procedure_type": "diagnostic",
        "likely_role_required": "operator",
        "summary": goal,
        "rough_steps": ["Open the screen.", "Review the value."],
        "related_artifact_ids": artifact_ids or [],
        "related_context_ids": context_ids or [],
        "source_refs": refs or [{"page": 1}],
        "evidence_source_refs": refs or [{"page": 1}],
        "source_id": f"source_{source_type}",
        "source_type": source_type,
        "ingestion_batch_id": "batch_test",
    }
