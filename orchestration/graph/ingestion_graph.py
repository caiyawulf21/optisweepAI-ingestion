from __future__ import annotations

from pathlib import Path

from langgraph.graph import END, START, StateGraph

from orchestration.graph.nodes import (
    assemble_delivery,
    classify_source,
    fail_unknown,
    finalize,
    publish_cosmos,
    route_after_assemble,
    route_after_classify,
    route_after_shared,
    route_after_source,
    run_incident,
    run_manual,
    run_shared_publish,
    run_training_video,
)
from orchestration.state import IngestionState


def build_ingestion_graph():
    graph = StateGraph(IngestionState)
    graph.add_node("classify_source", classify_source)
    graph.add_node("run_incident", run_incident)
    graph.add_node("run_manual", run_manual)
    graph.add_node("run_training_video", run_training_video)
    graph.add_node("fail_unknown", fail_unknown)
    graph.add_node("run_shared_publish", run_shared_publish)
    graph.add_node("assemble_delivery", assemble_delivery)
    graph.add_node("publish_cosmos", publish_cosmos)
    graph.add_node("finalize", finalize)

    graph.add_edge(START, "classify_source")
    graph.add_conditional_edges(
        "classify_source",
        route_after_classify,
        {
            "run_incident": "run_incident",
            "run_manual": "run_manual",
            "run_training_video": "run_training_video",
            "fail_unknown": "fail_unknown",
        },
    )
    for node in ("run_incident", "run_manual", "run_training_video", "fail_unknown"):
        graph.add_conditional_edges(
            node,
            route_after_source,
            {
                "run_shared_publish": "run_shared_publish",
                "assemble_delivery": "assemble_delivery",
                "finalize": "finalize",
            },
        )
    graph.add_conditional_edges(
        "run_shared_publish",
        route_after_shared,
        {
            "assemble_delivery": "assemble_delivery",
            "finalize": "finalize",
        },
    )
    graph.add_conditional_edges(
        "assemble_delivery",
        route_after_assemble,
        {
            "publish_cosmos": "publish_cosmos",
            "finalize": "finalize",
        },
    )
    graph.add_edge("publish_cosmos", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()


def run_ingestion(
    source_path: str | Path,
    *,
    companion_paths: list[str | Path] | None = None,
    output_dir: str | Path | None = None,
    source_stages: str | None = None,
    shared_stages: str | None = None,
    use_llm: bool = True,
    run_shared_publish: bool = False,
    publish_to_cosmos: bool = False,
    publish_scope: str = "all",
    ocr_backend: str = "azure_cv",
    max_workers: int = 4,
    source_title: str | None = None,
    source_id: str | None = None,
    source_roots: list[str | Path] | None = None,
) -> IngestionState:
    app = build_ingestion_graph()
    initial: IngestionState = {
        "source_path": str(Path(source_path).resolve()),
        "companion_paths": [str(Path(p).resolve()) for p in (companion_paths or [])],
        "use_llm": use_llm,
        "run_shared_publish": run_shared_publish,
        "publish_to_cosmos": publish_to_cosmos,
        "publish_scope": publish_scope,
        "ocr_backend": ocr_backend,
        "max_workers": max_workers,
        "status": "pending",
        "errors": [],
        "messages": [],
    }
    if output_dir is not None:
        initial["output_dir"] = str(Path(output_dir))
    if source_stages is not None:
        initial["source_stages"] = source_stages
    if shared_stages is not None:
        initial["shared_stages"] = shared_stages
    if source_title is not None:
        initial["source_title"] = source_title
    if source_id is not None:
        initial["source_id"] = source_id
    if source_roots is not None:
        initial["source_roots"] = [str(Path(p)) for p in source_roots]
    return app.invoke(initial)
