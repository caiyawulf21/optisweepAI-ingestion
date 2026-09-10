"""Decide whether a candidate name/description describes a real, look-up-able
named thing (an Entity) or a fact about one (a Claim).

The test (established while auditing brain/data/local/ontology_catalogs/
entities.json against real corpus content, see
brain/migration/BRAIN_BUILD_PROCESS.md): "is this a name someone would look
up, independent of any specific claim about it?" A screen, a database table,
a role, a model name -- yes, that's an Entity. A sentence describing what
something does, why it happens, or what a source said about it -- no, that's
a Claim about a real entity, and it belongs on that entity's record, not as
a new node of its own.

This started as Stage-4-context_type-based routing (operation_reference /
troubleshooting_reference -> Claim, everything else -> Entity). Auditing the
actual entity registry showed that was wrong: only 25% of the mis-modeled
entities came from those two context types. The rest was spread across
nearly every context type, plus entities created outside Stage 4 context
records entirely (the vision-promotion path). The routing has to be a
per-record content check, not a context_type lookup.
"""

from __future__ import annotations

import re

# Claim-verb constructions: paired with sentence structure (not just present
# as a word), these mark a name that asserts something about a subject
# rather than naming the subject itself.
_STRONG_CLAIM_VERB_RE = re.compile(
    r"\b(is used to|is used for|depends on|applies to|are separated|is discussed|"
    r"discussed in|describes?|explains?|indicates that|based on|associated with|"
    r"in relation to|relation to|limitations for|dependency on|behavior during|"
    r"behavior after|condition (associated|closes)|status associated)\b",
    re.IGNORECASE,
)

# A name starting with an imperative/instruction verb is a procedure title,
# not a thing's name.
_SENTENCE_START_RE = re.compile(
    r"^(Confirm|Check|Verify|Use|Using|Recover|Perform|Set|Install|Remove|Add|Apply|Execute|"
    r"System returns|System faults|Operator actions|Support is|Support access|Access control)\b"
)

# A name this long is a sentence almost by definition, regardless of other
# signals.
_VERY_LONG_WORD_COUNT = 9

# "X Overview" / "X Reference" / "X Troubleshooting" / "X Concept" as a
# SUFFIX after a specific noun phrase is usually a legitimate topic/screen/
# reference name ("ACB System Overview Screen", "Non-Recoverable Faults
# Overview") -- containing one of these words alone is not itself a signal.
_WEAK_SUFFIX_RE = re.compile(r"\b(overview|reference|troubleshooting|concept)\s*$", re.IGNORECASE)

# Evidence-reference language leaking into descriptive text ("the training
# slide presents...") instead of stating the fact directly. This is a
# cosmetic defect independent of the entity-vs-claim question -- it can flag
# on an otherwise-correct entity's description.
LEAK_RE = re.compile(r"\bthe (training )?(slide|transcript|segment|source|manual|artifact)\b", re.IGNORECASE)


def _word_count(name: str) -> int:
    return len(re.findall(r"\S+", name))


def is_claim_shaped(name: str) -> bool:
    """True if `name` reads as an assertion/procedure rather than a lookup-able name."""
    if _STRONG_CLAIM_VERB_RE.search(name):
        return True
    if _SENTENCE_START_RE.match(name):
        return True
    if _word_count(name) >= _VERY_LONG_WORD_COUNT:
        return True
    return False


def strip_source_reference_leak(text: str) -> str:
    """Rewrite descriptive text that frames itself as reporting what a source
    said into a direct statement of the fact, where that can be done safely
    by removing a leading frame without restructuring the sentence.

    Only handles the "The X states/notes/confirms that Y" and "According to
    the X, Y" shapes, where dropping the frame leaves Y as a complete,
    grammatical sentence on its own. Deliberately does NOT attempt "The X
    describes Y as Z" / "The X characterizes Y as Z" -- turning that into a
    natural "Y is Z" needs re-ordering the sentence around Y and Z, which a
    regex cannot do safely; those are left untouched rather than risk
    producing a grammatically broken description.
    """
    if not text:
        return text
    leading_frames = [
        r"^The (training )?(slide|transcript|segment|source|manual|artifact)s? (also )?"
        r"(states?|notes?|confirms?|explicitly states?|indicates?|says?|mentions?) that\s+",
        r"^According to the (training )?(slide|transcript|segment|source|manual|artifact),?\s+",
    ]
    rewritten = text
    for pattern in leading_frames:
        match = re.match(pattern, rewritten, re.IGNORECASE)
        if match:
            rewritten = rewritten[match.end():]
            if rewritten:
                rewritten = rewritten[0].upper() + rewritten[1:]
            break
    return rewritten
