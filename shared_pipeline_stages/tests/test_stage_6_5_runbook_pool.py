from __future__ import annotations

from pathlib import Path

from shared_pipeline_stages.stage_6_5.embedder import MockRunbookEmbedder
from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_6_5.pool_builder import PoolBuildConfig, build_runbook_pool
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, score_pair
from shared_pipeline_stages.stage_6_5.retrieval_card import build_retrieval_card


class HeartbeatTestEmbedder:
    @property
    def model_name(self) -> str:
        return "heartbeat-test-embedder"

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            lowered = text.lower()
            if "heartbeat" in lowered:
                vectors.append([1.0, 0.0, 0.0, 0.0])
            elif "start" in lowered:
                vectors.append([0.0, 1.0, 0.0, 0.0])
            elif "stop" in lowered:
                vectors.append([0.0, 0.0, 1.0, 0.0])
            else:
                vectors.append([0.0, 0.0, 0.0, 1.0])
        return vectors


def test_build_runbook_pool_writes_stage6_outputs(tmp_path: Path) -> None:
    source_root = tmp_path / "manual_optisweep_om_v3"
    finalized_dir = source_root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    finalized_dir.mkdir(parents=True)
    (finalized_dir / "candidate_manual_check_heartbeat.json").write_text(
        _runbook_json(
            procedure_id="proc_manual_check_heartbeat_v1",
            candidate_id="candidate_manual_check_heartbeat",
            title="Check Operator Station Heartbeat Stats",
            summary="Verify heartbeat timing between the tipper and WCS.",
            source_type="manual",
            source_id="manual_optisweep_om_v3",
        ),
        encoding="utf-8",
    )
    (finalized_dir / "candidate_incident_verify_heartbeat.json").write_text(
        _runbook_json(
            procedure_id="proc_incident_verify_heartbeat_v1",
            candidate_id="candidate_incident_verify_heartbeat",
            title="Verify Heartbeat Values",
            summary="Check heartbeat values on the operator station during a timeout investigation.",
            source_type="incident",
            source_id="case_228086",
        ),
        encoding="utf-8",
    )

    result = build_runbook_pool(
        source_roots=[source_root],
        output_dir=tmp_path / "shared",
        config=PoolBuildConfig(min_merge_score=0.3, high_confidence_score=0.5),
        embedder=HeartbeatTestEmbedder(),
        generated_at="2026-07-02T00:00:00Z",
    )

    stage_dir = tmp_path / "shared" / "stage_6_5_runbook_pool"
    assert result.runbook_count == 2
    assert result.merge_cluster_count == 1
    assert (stage_dir / "runbook_pool.json").exists()
    assert (stage_dir / "retrieval_cards.json").exists()
    assert (stage_dir / "runbook_retrieval_index.json").exists()
    assert (stage_dir / "merge_clusters.json").exists()
    assert (stage_dir / "pass_through_runbooks.json").exists()
    assert (stage_dir / "runbook_pool_report.json").exists()
    merge_clusters = read_json(stage_dir / "merge_clusters.json")
    assert merge_clusters[0]["requires_stage_7_llm"] is True
    report = read_json(stage_dir / "runbook_pool_report.json")
    assert report["combined_distribution"]["count"] >= 1


def test_opposing_actions_apply_penalty_not_hard_reject() -> None:
    start = build_retrieval_card(
        _runbook_dict(
            procedure_id="proc_start_v1",
            candidate_id="candidate_start",
            title="Start OptiSweep System",
            summary="Start the OptiSweep system.",
            source_type="manual",
            source_id="manual_optisweep_om_v3",
        )
    )
    stop = build_retrieval_card(
        _runbook_dict(
            procedure_id="proc_stop_v1",
            candidate_id="candidate_stop",
            title="Stop OptiSweep System",
            summary="Stop the OptiSweep system.",
            source_type="training_transcript",
            source_id="training_video_day1",
        )
    )
    embedder = HeartbeatTestEmbedder()
    vectors = embedder.embed_texts([start.retrieval_text, stop.retrieval_text])
    match = score_pair(start, stop, vectors[0], vectors[1], SimilarityConfig())
    assert match.opposing_actions_detected is True
    assert match.combined_score >= 0.0


def test_same_source_pairs_do_not_form_merge_cluster(tmp_path: Path) -> None:
    source_root = tmp_path / "manual_optisweep_om_v3"
    finalized_dir = source_root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    finalized_dir.mkdir(parents=True)
    for index, title in enumerate(["Check Alarms A", "Check Alarms B"], start=1):
        (finalized_dir / f"candidate_{index}.json").write_text(
            _runbook_json(
                procedure_id=f"proc_check_alarms_{index}_v1",
                candidate_id=f"candidate_check_alarms_{index}",
                title=title,
                summary="Review active operator station alarms.",
                source_type="manual",
                source_id="manual_optisweep_om_v3",
            ),
            encoding="utf-8",
        )

    result = build_runbook_pool(
        source_roots=[source_root],
        output_dir=tmp_path / "shared",
        config=PoolBuildConfig(min_merge_score=0.1),
        embedder=MockRunbookEmbedder(dimensions=8),
    )
    assert result.merge_cluster_count == 0
    merge_clusters = read_json(tmp_path / "shared" / "stage_6_5_runbook_pool" / "merge_clusters.json")
    assert merge_clusters == []


def _runbook_json(
    *,
    procedure_id: str,
    candidate_id: str,
    title: str,
    summary: str,
    source_type: str,
    source_id: str,
) -> str:
    import json

    return json.dumps(
        _runbook_dict(
            procedure_id=procedure_id,
            candidate_id=candidate_id,
            title=title,
            summary=summary,
            source_type=source_type,
            source_id=source_id,
        )
    )


def _runbook_dict(
    *,
    procedure_id: str,
    candidate_id: str,
    title: str,
    summary: str,
    source_type: str,
    source_id: str,
) -> dict:
    return {
        "procedure_id": procedure_id,
        "candidate_id": candidate_id,
        "title": title,
        "summary": summary,
        "procedure_type": "diagnostic",
        "role_required": "operator",
        "when_to_use": summary,
        "steps": [
            {
                "step_number": 1,
                "title": "Review values",
                "instruction": "Open the screen and review the value.",
            }
        ],
        "source_candidate_ids": [candidate_id],
        "validation_status": "needs_sme_review",
        "metadata": {
            "merge_status": "source_finalized",
            "source_id": source_id,
            "source_type": source_type,
        },
        "source_lineage": [
            {
                "source_id": source_id,
                "source_type": source_type,
            }
        ],
    }
