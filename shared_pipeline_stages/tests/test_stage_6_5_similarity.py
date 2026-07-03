from shared_pipeline_stages.stage_6_5.similarity import STOPWORDS, token_jaccard


def test_jaccard_excludes_stopwords_and_is_order_independent() -> None:
    first = "Check the AGV status on the RMS page"
    second = "RMS page AGV status check"
    reordered = "status AGV check RMS page"
    assert token_jaccard(first, second) == token_jaccard(first, reordered)
    score = token_jaccard(first, second)
    assert score > 0.0
    only_stopwords = " ".join(sorted(STOPWORDS))
    assert token_jaccard(only_stopwords, only_stopwords) == 0.0


def test_jaccard_normalizes_verify_and_check() -> None:
    verify_text = "Verify heartbeat on the operator station"
    check_text = "Check heartbeat on operator station"
    unrelated = "Install gripper replacement motor"
    assert token_jaccard(verify_text, check_text) > token_jaccard(verify_text, unrelated)
