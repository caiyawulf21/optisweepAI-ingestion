from __future__ import annotations

from pathlib import Path

from shared_pipeline_stages.stage_6_5.json_utils import read_json
from shared_pipeline_stages.stage_6_5.pool_builder import PoolBuildConfig, build_runbook_pool
from shared_pipeline_stages.stage_6_5.schemas import MergeCluster, PairwiseMatch
from shared_pipeline_stages.stage_7.cluster_split import build_sub_clusters, split_oversized_cluster
from shared_pipeline_stages.stage_7.merge_builder import Stage7BuildConfig, build_stage7_merged_runbooks
from shared_pipeline_stages.stage_7.normalize import canonical_procedure_id, normalize_merged_runbook
from shared_pipeline_stages.stage_7.pass_through import promote_pass_through_runbook


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
            elif "unique manual" in lowered:
                vectors.append([0.0, 0.0, 0.0, 1.0])
            else:
                vectors.append([0.0, 0.0, 0.0, 1.0])
        return vectors


class FakeMergeClient:
    def merge(self, packet: dict) -> dict:
        runbooks = packet.get("finalized_runbooks") or []
        title = str(runbooks[0].get("title") or "Merged Procedure")
        return {
            "merge_decision": "merged",
            "canonical_runbooks": [
                {
                    "procedure_id": canonical_procedure_id(title),
                    "title": title,
                    "procedure_type": "diagnostic",
                    "role_required": "operator",
                    "summary": "Merged summary",
                    "when_to_use": "Merged when needed",
                    "steps": [
                        {
                            "step_number": 1,
                            "title": "Merged step",
                            "instruction": "Perform merged action.",
                            "expected_result": "Merged result.",
                            "responsible_role": "operator",
                        }
                    ],
                    "merged_from_procedure_ids": [
                        str(item.get("procedure_id") or "") for item in runbooks
                    ],
                }
            ],
            "conflicts": [],
            "known_gaps": [],
            "merge_notes": ["Fake merge for test."],
        }


def test_split_oversized_cluster_into_groups_of_three() -> None:
    members = [f"proc_{index}_v1" for index in range(6)]
    matches = [
        PairwiseMatch(
            source_id=members[0],
            target_id=members[1],
            cosine_score=0.9,
            jaccard_score=0.8,
            combined_score=0.86,
        ),
        PairwiseMatch(
            source_id=members[2],
            target_id=members[3],
            cosine_score=0.88,
            jaccard_score=0.75,
            combined_score=0.84,
        ),
        PairwiseMatch(
            source_id=members[4],
            target_id=members[5],
            cosine_score=0.87,
            jaccard_score=0.7,
            combined_score=0.82,
        ),
    ]
    cluster = MergeCluster(
        merge_cluster_id="cluster_test",
        finalized_runbook_ids=members,
        candidate_ids=[f"candidate_{index}" for index in range(6)],
        source_types=["manual", "training_video"],
        similarity_score=0.86,
        merge_hint="needs_review",
        pairwise_matches=matches,
    )
    groups = split_oversized_cluster(cluster, max_size=3)
    assert len(groups) == 3
    assert all(len(group) <= 3 for group in groups)
    assert sorted(member for group in groups for member in group) == sorted(members)


def test_build_sub_clusters_marks_auto_split() -> None:
    members = [f"proc_{index}_v1" for index in range(4)]
    cluster = MergeCluster(
        merge_cluster_id="cluster_test",
        finalized_runbook_ids=members,
        candidate_ids=[f"candidate_{index}" for index in range(4)],
        source_types=["manual", "training_video"],
        similarity_score=0.7,
        merge_hint="needs_review",
        pairwise_matches=[
            PairwiseMatch(
                source_id=members[0],
                target_id=members[1],
                cosine_score=0.8,
                jaccard_score=0.6,
                combined_score=0.74,
            )
        ],
    )
    sub_clusters = build_sub_clusters(cluster, max_size=3)
    assert len(sub_clusters) >= 2
    assert any("Auto-split" in note for sub in sub_clusters for note in sub.evidence_notes)


def test_stage7_dry_run_promotes_pass_through_only(tmp_path: Path) -> None:
    pool_dir = _build_pool_fixture(tmp_path)
    result = build_stage7_merged_runbooks(
        pool_dir=pool_dir,
        output_dir=tmp_path / "shared",
        config=Stage7BuildConfig(max_cluster_size=3, llm_used=False),
        generated_at="2026-07-05T00:00:00Z",
    )
    stage_dir = tmp_path / "shared" / "stage_7_merged_runbooks"
    canonical = read_json(stage_dir / "canonical_runbooks.json")
    mappings = read_json(stage_dir / "candidate_to_procedure_mapping.json")
    packets = read_json(stage_dir / "merge_packets.json")
    assert result.pass_through_count == 1
    assert result.canonical_runbook_count == 1
    assert len(canonical["runbooks"]) == 1
    assert canonical["runbooks"][0]["metadata"]["merge_status"] == "pass_through"
    assert len(mappings["mappings"]) == 1
    assert len(packets) == 1
    assert len(packets[0]["finalized_runbooks"]) == 2


def test_stage7_llm_merge_writes_new_canonical_id_and_references(tmp_path: Path) -> None:
    pool_dir = _build_pool_fixture(tmp_path)
    result = build_stage7_merged_runbooks(
        pool_dir=pool_dir,
        output_dir=tmp_path / "shared",
        config=Stage7BuildConfig(max_cluster_size=3, llm_used=True),
        llm_client=FakeMergeClient(),
        generated_at="2026-07-05T00:00:00Z",
    )
    stage_dir = tmp_path / "shared" / "stage_7_merged_runbooks"
    canonical = read_json(stage_dir / "canonical_runbooks.json")
    mappings = read_json(stage_dir / "candidate_to_procedure_mapping.json")
    assert result.llm_merge_count == 1
    merged = [item for item in canonical["runbooks"] if item["metadata"]["merge_status"] == "canonical"]
    assert len(merged) == 1
    assert merged[0]["procedure_id"].endswith("_canonical_v1")
    assert len(merged[0]["merged_from_procedure_ids"]) == 2
    assert len([item for item in mappings["mappings"] if item["merge_action"] == "merged"]) == 2


def test_promote_pass_through_keeps_procedure_id() -> None:
    runbook = {
        "procedure_id": "proc_manual_check_heartbeat_v1",
        "candidate_id": "candidate_manual_check_heartbeat",
        "title": "Check Heartbeat",
        "summary": "Check heartbeat",
        "steps": [{"step_number": 1, "title": "Check", "instruction": "Check"}],
        "metadata": {"merge_status": "source_finalized", "source_type": "manual"},
    }
    promoted = promote_pass_through_runbook(runbook)
    assert promoted["procedure_id"] == "proc_manual_check_heartbeat_v1"
    assert promoted["metadata"]["merge_status"] == "pass_through"


def test_normalize_merged_runbook_assigns_new_id_and_references() -> None:
    source_runbooks = [
        {
            "procedure_id": "proc_manual_check_heartbeat_v1",
            "candidate_id": "candidate_manual_check_heartbeat",
            "title": "Check Heartbeat Manual",
            "summary": "Manual summary",
            "procedure_type": "diagnostic",
            "role_required": "operator",
            "steps": [{"step_number": 1, "title": "A", "instruction": "A"}],
        },
        {
            "procedure_id": "proc_incident_verify_heartbeat_v1",
            "candidate_id": "candidate_incident_verify_heartbeat",
            "title": "Verify Heartbeat Incident",
            "summary": "Incident summary",
            "procedure_type": "diagnostic",
            "role_required": "operator",
            "steps": [{"step_number": 1, "title": "B", "instruction": "B"}],
        },
    ]
    normalized = normalize_merged_runbook(
        {"title": "Check Heartbeat Manual", "steps": source_runbooks[0]["steps"]},
        source_runbooks=source_runbooks,
        merge_cluster_id="cluster_test",
        sub_cluster_id="cluster_test__sub_1",
        merge_decision="merged",
    )
    assert normalized["procedure_id"].endswith("_canonical_v1")
    assert set(normalized["merged_from_procedure_ids"]) == {
        "proc_manual_check_heartbeat_v1",
        "proc_incident_verify_heartbeat_v1",
    }


def _build_pool_fixture(tmp_path: Path) -> Path:
    manual_root = tmp_path / "manual_optisweep_om_v3"
    incident_root = tmp_path / "case_228086"
    manual_dir = manual_root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    incident_dir = incident_root / "stage_6_finalized_runbooks" / "finalized_runbooks"
    manual_dir.mkdir(parents=True)
    incident_dir.mkdir(parents=True)
    manual_path = manual_dir / "candidate_manual_check_heartbeat.json"
    incident_path = incident_dir / "candidate_incident_verify_heartbeat.json"
    manual_path.write_text(_runbook_json(
        procedure_id="proc_manual_check_heartbeat_v1",
        candidate_id="candidate_manual_check_heartbeat",
        title="Check Operator Station Heartbeat Stats",
        summary="Verify heartbeat timing between the tipper and WCS.",
        source_type="manual",
        source_id="manual_optisweep_om_v3",
    ), encoding="utf-8")
    incident_path.write_text(_runbook_json(
        procedure_id="proc_incident_verify_heartbeat_v1",
        candidate_id="candidate_incident_verify_heartbeat",
        title="Verify Heartbeat Values",
        summary="Check heartbeat values on the operator station during a timeout investigation.",
        source_type="incident",
        source_id="case_228086",
    ), encoding="utf-8")
    unique_path = manual_dir / "candidate_manual_unique_only.json"
    unique_path.write_text(_runbook_json(
        procedure_id="proc_manual_unique_only_v1",
        candidate_id="candidate_manual_unique_only",
        title="Unique Manual Procedure",
        summary="Unique manual-only reference with no cross-source match.",
        source_type="manual",
        source_id="manual_optisweep_om_v3",
    ), encoding="utf-8")

    pool_output = tmp_path / "shared"
    build_runbook_pool(
        source_roots=[manual_root, incident_root],
        output_dir=pool_output,
        config=PoolBuildConfig(min_merge_score=0.3, high_confidence_score=0.5),
        embedder=HeartbeatTestEmbedder(),
        generated_at="2026-07-05T00:00:00Z",
    )
    return pool_output / "stage_6_5_runbook_pool"


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
        {
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
                    "expected_result": "Value is visible.",
                    "responsible_role": "operator",
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
    )
