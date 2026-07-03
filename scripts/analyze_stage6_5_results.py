from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for candidate in (
    REPO / "data" / "output" / "shared" / "stage_6_5_runbook_pool",
    REPO / "shared_pipeline_stages" / "data" / "output" / "shared" / "stage_6_5_runbook_pool",
):
    if (candidate / "runbook_pool_report.json").exists():
        BASE = candidate
        break
else:
    raise FileNotFoundError("Stage 6.5 output directory not found")


def main() -> None:
    report = json.loads((BASE / "runbook_pool_report.json").read_text(encoding="utf-8"))
    pool = json.loads((BASE / "runbook_pool.json").read_text(encoding="utf-8"))
    merge = json.loads((BASE / "merge_clusters.json").read_text(encoding="utf-8"))
    pt = json.loads((BASE / "pass_through_runbooks.json").read_text(encoding="utf-8"))
    sim = json.loads((BASE / "runbook_similarity.json").read_text(encoding="utf-8"))
    cards = {c["finalized_runbook_id"]: c for c in json.loads((BASE / "retrieval_cards.json").read_text(encoding="utf-8"))}

    entries = pool["entries"]
    id_to_title = {e["finalized_runbook_id"]: e["title"] for e in entries}

    print("=== POOL SUMMARY ===")
    print(f"runbooks: {len(entries)}")
    print(f"merge_clusters: {len(merge)}")
    print(f"pass_through: {len(pt)}")
    print(f"embedding_model: {report['embedding_model']}")
    print(f"embeddings_generated: {report['embeddings_generated']}")
    print(f"warnings: {len(report.get('warnings', []))}")

    print("\n=== SOURCE TYPE COUNTS ===")
    for source_type, count in Counter(e["source_type"] for e in entries).most_common():
        print(f"  {source_type}: {count}")

    print("\n=== PASS-THROUGH REASONS ===")
    for reason, count in Counter(p["pass_through_reason"] for p in pt).most_common():
        print(f"  {reason}: {count}")

    print("\n=== SCORE DISTRIBUTIONS ===")
    for name in ("cosine_distribution", "jaccard_distribution", "combined_distribution"):
        d = report[name]
        print(f"  {name}: count={d['count']} min={d.get('min')} max={d.get('max')} mean={d.get('mean')} p50={d.get('p50')} p95={d.get('p95')}")

    print("\n=== MERGE CLUSTERS ===")
    for cluster in merge:
        print(f"\n  {cluster['merge_cluster_id']}")
        print(f"    size={len(cluster['finalized_runbook_ids'])} score={cluster['similarity_score']} hint={cluster['merge_hint']}")
        print(f"    sources={cluster['source_types']}")
        for rid in cluster["finalized_runbook_ids"]:
            card = cards.get(rid, {})
            print(f"      - [{card.get('source_type','')}] {id_to_title.get(rid, rid)}")

    match_counts = [len(e.get("top_cross_source_matches", [])) for e in sim]
    print("\n=== CROSS-SOURCE MATCH COVERAGE ===")
    print(f"  runbooks with 0 matches above threshold: {sum(1 for x in match_counts if x == 0)}")
    print(f"  runbooks with 1+ matches: {sum(1 for x in match_counts if x > 0)}")
    print(f"  max matches on one runbook: {max(match_counts) if match_counts else 0}")

    print("\n=== TOP 15 CROSS-SOURCE PAIRS ===")
    pairs = report.get("top_cross_source_pairs", [])
    for match in pairs[:15]:
        src_title = id_to_title.get(match["source_id"], match["source_id"])[:55]
        tgt_title = id_to_title.get(match["target_id"], match["target_id"])[:55]
        warnings = match.get("metadata_warnings") or []
        warn = f" | {warnings[0]}" if warnings else ""
        print(f"  {match['combined_score']:.4f} (c={match['cosine_score']}, j={match['jaccard_score']}){warn}")
        print(f"    {src_title}")
        print(f"    -> {tgt_title}")

    print("\n=== INCIDENT RUNBOOK ===")
    for entry in entries:
        if "incident" in entry.get("source_type", ""):
            rid = entry["finalized_runbook_id"]
            matches = next((x for x in sim if x["finalized_runbook_id"] == rid), {})
            top = matches.get("top_cross_source_matches", [])
            print(f"  {entry['title']}")
            print(f"  pass_through: {next((p['pass_through_reason'] for p in pt if p['finalized_runbook_id']==rid), '?')}")
            print(f"  cross-source matches above threshold: {len(top)}")
            for match in top[:5]:
                print(f"    {match['combined_score']:.4f} -> {id_to_title.get(match['target_id'], match['target_id'])[:60]}")

    print("\n=== SKIPPED DUPLICATES ===")
    for warning in report.get("warnings", []):
        print(f"  {warning.split(' from ')[-1] if ' from ' in warning else warning}")


if __name__ == "__main__":
    main()
