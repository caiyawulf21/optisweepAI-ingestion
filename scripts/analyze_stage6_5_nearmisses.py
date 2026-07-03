from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
for candidate in (
    REPO / "data" / "output" / "shared" / "stage_6_5_runbook_pool",
    REPO / "shared_pipeline_stages" / "data" / "output" / "shared" / "stage_6_5_runbook_pool",
):
    if (candidate / "runbook_pool.json").exists():
        BASE = candidate
        break
else:
    raise FileNotFoundError("Stage 6.5 output not found")

from shared_pipeline_stages.stage_6_5.retriever import InMemoryRunbookRetriever
from shared_pipeline_stages.stage_6_5.schemas import RetrievalCard
from shared_pipeline_stages.stage_6_5.similarity import SimilarityConfig, score_pair


def main() -> None:
    cards = json.loads((BASE / "retrieval_cards.json").read_text(encoding="utf-8"))
    index = json.loads((BASE / "runbook_retrieval_index.json").read_text(encoding="utf-8"))
    pool = json.loads((BASE / "runbook_pool.json").read_text(encoding="utf-8"))
    id_to_title = {e["finalized_runbook_id"]: e["title"] for e in pool["entries"]}

    vectors = {entry["finalized_runbook_id"]: entry["vector"] for entry in index}
    typed_cards = [RetrievalCard.model_validate(c) for c in cards]
    config = SimilarityConfig()
    retriever = InMemoryRunbookRetriever(typed_cards, vectors, config)

    incident_id = "proc_restart_ignition_and_verify_optisweep_service_response_with_getagvstatuses_v1"
    incident = next(c for c in typed_cards if c.finalized_runbook_id == incident_id)
    print("=== INCIDENT NEAR-MISSES (min_score=0) ===")
    matches = retriever.search(incident, top_k=10, min_score=0.0, cross_source_only=True)
    for match in matches[:8]:
        print(f"  {match.combined_score:.4f} (c={match.cosine_score}, j={match.jaccard_score})")
        print(f"    -> {id_to_title.get(match.target_id, match.target_id)[:70]}")

    print("\n=== AGV CLUSTER WEAKEST LINK ===")
    agv_ids = [
        "proc_check_current_agv_system_status_using_the_rms_page_v1",
        "proc_open_the_agv_status_screen_and_check_agv_locations_and_current_error_codes_v1",
    ]
    a = next(c for c in typed_cards if c.finalized_runbook_id == agv_ids[0])
    b = next(c for c in typed_cards if c.finalized_runbook_id == agv_ids[1])
    match = score_pair(a, b, vectors[agv_ids[0]], vectors[agv_ids[1]], config)
    print(f"  RMS page <-> AGV status screen: combined={match.combined_score} cosine={match.cosine_score} jaccard={match.jaccard_score}")
    print(f"  threshold=0.62 -> {'IN cluster' if match.combined_score >= 0.62 else 'OUT'}")

    print("\n=== PAIRS JUST BELOW 0.62 THRESHOLD (sample) ===")
    below: list = []
    for left in typed_cards:
        for right in typed_cards:
            if left.finalized_runbook_id >= right.finalized_runbook_id:
                continue
            if left.source_type == right.source_type:
                continue
            match = score_pair(
                left, right,
                vectors[left.finalized_runbook_id],
                vectors[right.finalized_runbook_id],
                config,
            )
            if 0.55 <= match.combined_score < 0.62:
                below.append(match)
    below.sort(key=lambda m: -m.combined_score)
    for match in below[:8]:
        print(f"  {match.combined_score:.4f} | {id_to_title.get(match.source_id,'')[:45]}")
        print(f"           -> {id_to_title.get(match.target_id,'')[:45]}")


if __name__ == "__main__":
    main()
