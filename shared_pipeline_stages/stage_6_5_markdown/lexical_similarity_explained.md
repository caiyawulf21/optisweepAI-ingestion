# Lexical Similarity Explained (Stage 6.5)

Stage 6.5 hybrid retrieval combines **Azure embedding cosine similarity** with **token
Jaccard similarity** on the same `retrieval_text` field.

## Lexical is NOT exact-phrase or order-based

The lexical score does **not** require:

- the same words in the same order
- contiguous phrase matches
- all tokens from the text

It **does** require overlap among **meaningful tokens** extracted from both runbooks'
`retrieval_text` strings.

Implementation: `score_pair()` → `token_jaccard()` in
[`shared_pipeline_stages/stage_6_5/similarity.py`](../stage_6_5/similarity.py).

## Pipeline: text → tokens → Jaccard

```text
retrieval_text (both runbooks)
       ↓
lowercase, split on words/numbers
       ↓
remove STOPWORDS and tokens with length ≤ 1
       ↓
normalize action synonyms (verify/review/inspect → check)
       ↓
meaningful token sets A and B
       ↓
jaccard = |A ∩ B| / |A ∪ B|
```

### Stopwords excluded

These tokens are **never** counted for lexical overlap:

```text
a, an, and, for, in, of, on, the, to, use, using, with
```

Defined in `STOPWORDS` in `similarity.py`.

### Length filter

Tokens with **length ≤ 1** after splitting are dropped (e.g. single letters).

### Action synonym normalization

Before set comparison, these tokens are mapped to a canonical action:

| Token(s) | Normalized to |
| --- | --- |
| check, verify, review, inspect | check |
| start, starting | start |
| stop, stopping, shutdown | stop |
| add | add |
| remove | remove |

So manual "Verify heartbeat" and training "Check heartbeat" share the token `check`.

## Worked example

**Runbook A retrieval text (simplified):**  
`Check AGV status on the RMS page for errors`

**Runbook B retrieval text (simplified):**  
`Review fleet AGV status screen for error codes`

**Meaningful tokens A (approx):**  
`{check, agv, status, rms, page, errors}`

**Meaningful tokens B (approx):**  
`{check, fleet, agv, status, screen, error, codes}`

Note: `the`, `on`, `for` are removed as stopwords. `Review` → `check`.

**Intersection:** `{check, agv, status, errors}` (and possibly `error`/`errors` as distinct tokens)

**Union:** all unique meaningful tokens from both sides

**Jaccard** = intersection size / union size → typically **0.2–0.4** for related
manual/training pairs in our corpus (exact value depends on full step text).

## What lexical catches vs vector

| Lexical (Jaccard) | Vector (cosine) |
| --- | --- |
| Shared screen names, commands, component IDs | Paraphrases and different wording |
| Exact domain terms (AGV, RMS, HMI) | Semantic similarity when words differ |
| Weak when wording diverges but meaning matches | Can over-match broad domain vocabulary |

## Verification in code

Call chain verified:

1. `score_pair()` calls `token_jaccard(first.retrieval_text, second.retrieval_text)`
2. `token_jaccard()` calls `_meaningful_tokens()` on each string
3. `_meaningful_tokens()` applies `STOPWORDS`, length > 1, and `ACTION_EQUIVALENTS`

Unit test: `shared_pipeline_stages/tests/test_stage_6_5_similarity.py::test_jaccard_excludes_stopwords_and_is_order_independent`
