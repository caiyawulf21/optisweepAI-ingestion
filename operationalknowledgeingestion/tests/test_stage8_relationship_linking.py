from optisweep_ingestion.stage8_relationship_linking import link_source_relationships
from optisweep_ingestion.tools.relationship_linker import (
    apply_relationship_links,
    artifact_ids_from_runbook,
    build_relationship_links,
)


def _heartbeat_fixture() -> tuple[list[dict], list[dict], list[dict]]:
    artifact_id = "artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats"
    context_id = "ctx_manual_visu_data_heartbeat_stats_v1"
    procedure_id = "proc_review_heartbeat_statistics_on_the_visu_data_screen_v1"
    candidate_id = "candidate_l1_review_heartbeat_stats_on_visu_data_screen"

    artifacts = [
        {
            "artifact_id": artifact_id,
            "title": "Operator Station HMI Data Screen — Heartbeat Stats",
            "linked_context_ids": [],
            "linked_runbook_ids": [],
            "linked_procedure_ids": [],
        }
    ]
    contexts = [
        {
            "context_id": context_id,
            "title": "VISU_DATA Heartbeat statistics between tipper and WCS",
            "related_artifact_ids": [artifact_id],
            "image_refs": [artifact_id],
            "related_runbook_candidate_ids": [candidate_id],
        }
    ]
    runbooks = [
        {
            "procedure_id": procedure_id,
            "candidate_id": candidate_id,
            "title": "Review Heartbeat Statistics On The VISU_DATA Screen",
            "related_context_ids": [context_id],
            "visual_references": [
                {
                    "artifact_id": artifact_id,
                    "description": "Heartbeat section on the VISU_DATA screen.",
                }
            ],
            "steps": [
                {
                    "step_number": 1,
                    "screens_or_images": [{"artifact_id": artifact_id, "what_to_look_at": ["Last", "Max", "Min"]}],
                }
            ],
        }
    ]
    return artifacts, contexts, runbooks


def test_heartbeat_example_links_artifact_context_and_runbook() -> None:
    artifacts, contexts, runbooks = _heartbeat_fixture()
    links, payload = build_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        candidates=[{"candidate_id": runbooks[0]["candidate_id"], "related_context_ids": [contexts[0]["context_id"]]}],
    )
    linked_artifacts, linked_contexts, linked_runbooks = apply_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        adjacency=payload["adjacency"],
    )

    artifact = linked_artifacts[0]
    context = linked_contexts[0]
    runbook = linked_runbooks[0]

    assert context["context_id"] in artifact["linked_context_ids"]
    assert runbook["procedure_id"] in artifact["linked_runbook_ids"]
    assert runbook["procedure_id"] in artifact["linked_procedure_ids"]
    assert runbook["procedure_id"] in context["related_runbook_ids"]
    assert artifact["artifact_id"] in runbook["linked_artifact_ids"]
    assert any(link["link_type"] == "artifact_context" for link in links)
    assert any(link["link_type"] == "artifact_runbook" for link in links)
    assert any(link["link_type"] == "context_runbook" for link in links)


def test_shared_artifact_inference_links_context_to_runbook_without_direct_context_ref() -> None:
    artifact_id = "artifact_fig_4_22_operator_station_hmi_data_screen_heartbeat_stats"
    context_id = "ctx_manual_visu_data_heartbeat_stats_v1"
    procedure_id = "proc_review_heartbeat_statistics_on_the_visu_data_screen_v1"

    artifacts = [{"artifact_id": artifact_id, "linked_context_ids": [], "linked_runbook_ids": [], "linked_procedure_ids": []}]
    contexts = [
        {
            "context_id": context_id,
            "related_artifact_ids": [artifact_id],
            "image_refs": [artifact_id],
            "related_runbook_candidate_ids": [],
        }
    ]
    runbooks = [
        {
            "procedure_id": procedure_id,
            "candidate_id": "candidate_l1_review_heartbeat_stats_on_visu_data_screen",
            "related_context_ids": [],
            "visual_references": [{"artifact_id": artifact_id}],
            "steps": [],
        }
    ]

    links, payload = build_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        infer_shared_artifact_links=True,
    )
    linked_artifacts, linked_contexts, _ = apply_relationship_links(
        artifacts=artifacts,
        contexts=contexts,
        runbooks=runbooks,
        adjacency=payload["adjacency"],
    )

    assert procedure_id in linked_contexts[0]["related_runbook_ids"]
    assert procedure_id in linked_artifacts[0]["linked_runbook_ids"]
    assert any(link["link_type"] == "context_runbook_shared_artifact" for link in links)


def test_artifact_ids_from_runbook_collects_step_and_visual_refs() -> None:
    runbook = {
        "visual_references": [{"artifact_id": "artifact_a"}],
        "steps": [{"screens_or_images": [{"artifact_id": "artifact_b"}]}],
    }
    assert artifact_ids_from_runbook(runbook) == ["artifact_a", "artifact_b"]


def test_stage8_end_to_end_writes_outputs(tmp_path) -> None:
    output_dir = tmp_path / "manual_optisweep_om_v3"
    artifacts, contexts, runbooks = _heartbeat_fixture()

    from optisweep_ingestion.stage_paths import stage_dir
    from optisweep_ingestion.utils.json_utils import write_json

    write_json(stage_dir(output_dir, "3") / "source_artifacts_enriched.json", artifacts)
    write_json(stage_dir(output_dir, "4") / "operational_context.json", contexts)
    runbooks_dir = stage_dir(output_dir, "6") / "finalized_runbooks"
    runbooks_dir.mkdir(parents=True, exist_ok=True)
    write_json(runbooks_dir / f"{runbooks[0]['candidate_id']}.json", runbooks[0])
    write_json(
        stage_dir(output_dir, "5") / "runbook_candidates.json",
        [{"candidate_id": runbooks[0]["candidate_id"], "related_context_ids": [contexts[0]["context_id"]]}],
    )

    report = link_source_relationships(output_dir=output_dir)
    stage8_dir = stage_dir(output_dir, "8")

    assert (stage8_dir / "relationship_links.json").exists()
    assert (stage8_dir / "source_artifacts_linked.json").exists()
    assert (stage8_dir / "operational_context_linked.json").exists()
    assert (stage8_dir / "relationship_linking_report.json").exists()
    assert (stage8_dir / "finalized_runbooks_linked.json").exists()
    assert report["link_stats"]["link_count"] >= 3
