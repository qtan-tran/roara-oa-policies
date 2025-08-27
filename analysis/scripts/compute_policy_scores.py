"""
compute_policy_scores.py
========================

This script traverses all plain‑text policy files in the
`policies/text/` directory and attempts to automatically classify
each policy’s provisions according to the eight conditions defined
in Vincent–Lamarre et al. (2015) for estimating Open Access (OA)
mandate strength.  The conditions (C1–C8) cover mandate language,
opt‑out provisions, versions allowed, deposit timing, embargo
length, copyright, internal use, and whether the policy also
applies to theses.

For each condition the script uses a simple set of keyword and
regular expression rules to extract a numeric value reflecting the
strength of that condition.  Because institutional policies are
written in a variety of styles and languages, these rules are
necessarily heuristic and will occasionally misclassify passages.
However, they provide a fully reproducible baseline that can be
iteratively refined.  The detected values are subsequently
normalised to the [0, 1] range and combined using the weights from
the original MELIBEA scoring formula to produce an “initial”
mandate strength (0–100 %).  A simplified “updated” score is also
computed that emphasises the conditions empirically shown in the
paper to be most predictive of deposit behaviour (C2, C4 and C7),
with the other conditions given zero weight.

The resulting scores are written to a CSV file under
`analysis/outputs/tables/policy_scores.csv` and printed to the
console.  A tab‑separated version (`policy_scores.tsv`) is also
written to the same directory so that the QA linter can discover
and validate it automatically.  Policies that cannot be read will be
skipped with a warning.

Usage
-----
Run this script from the repository root or directly via

    python analysis/scripts/compute_policy_scores.py

The script has no command‑line arguments.

"""

import csv
import os
import re
from pathlib import Path
from typing import Dict, Tuple


###############################################################################
# Configuration
###############################################################################

# Directory containing the plain‑text policy files.  This is resolved
# relative to the script’s location so it works regardless of the
# current working directory.
POLICIES_DIR = Path(__file__).resolve().parents[2] / "policies" / "text"

# Output CSV file.  It will be created (along with any missing
# parent directories) if necessary.
OUTPUT_CSV = (
    Path(__file__).resolve().parents[2]
    / "analysis"
    / "outputs"
    / "tables"
    / "policy_scores.csv"
)

# Weights for the initial MELIBEA formula (sum to 1.0).  The keys
# correspond to conditions C1–C8.  See Vincent‑Lamarre et al. (2015)
# for details.
INITIAL_WEIGHTS: Dict[str, float] = {
    "C1": 0.40,  # Mandate vs request
    "C2": 0.10,  # Opt‑out
    "C3": 0.05,  # Version
    "C4": 0.10,  # Deposit timing
    "C5": 0.10,  # Embargo length
    "C6": 0.10,  # Copyright
    "C7": 0.10,  # Internal use
    "C8": 0.10,  # Theses
}

# For the simplified updated formula we follow the paper’s
# observation that deposit timing (C4), internal use (C7) and the
# nature of the opt‑out (C2) correlate strongest with deposit
# behaviour.  Consequently only those three conditions contribute,
# with equal weight, while the remainder have weight zero.  The
# weights sum to 1.0.
UPDATED_WEIGHTS: Dict[str, float] = {
    "C1": 0.0,
    "C2": 1.0 / 3.0,
    "C3": 0.0,
    "C4": 1.0 / 3.0,
    "C5": 0.0,
    "C6": 0.0,
    "C7": 1.0 / 3.0,
    "C8": 0.0,
}

# Minimum and maximum possible values for each condition.  These
# bounds are used to normalise raw values to the [0, 1] interval.
# See the specification in the problem statement for the allowed
# options and their associated values.
CONDITION_BOUNDS: Dict[str, Tuple[float, float]] = {
    "C1": (1, 2),    # Request (1) – Requirement (2)
    "C2": (-1, 2),   # Deposit opt‑out & OA opt‑out (−1) – No deposit opt‑out with OA opt‑out (2)
    "C3": (0, 0.8),  # Unspecified (0) – Author/publisher version (0.8)
    "C4": (0, 2),    # Unspecified (0) – At time of acceptance (2)
    "C5": (-2, 0.5), # 12+ months or unspecified (−2) – 6 months (0.5)
    "C6": (-2, 2),   # No copyright reservation (−2) – Strong rights retention (2)
    "C7": (0, 2),    # Internal use not specified (0) – Yes (2)
    "C8": (0, 2),    # Theses not covered (0) – Covered (2)
}


###############################################################################
# Heuristic classification functions
###############################################################################

def classify_c1(text: str) -> float:
    """Classify mandate vs request (C1).

    If the policy uses strong, binding language (e.g. “must”,
    “required”, “shall”) in conjunction with deposit/self‑archiving,
    it is treated as a requirement (2).  If it uses weaker
    language (e.g. “should”, “encourage”, “recommend”), it is treated
    as a request (1).  Otherwise the condition is assumed not to be
    specified and defaults to the minimum (1).

    The search is case‑insensitive and looks for both English and
    German key words.
    """
    t = text.lower()
    # Strong mandate words
    strong_patterns = [
        r"\bmust\b",
        r"\bshall\b",
        r"\bar[e]? required\b",
        r"\brequirement\b",
        r"\bverpflichtet\b",  # German: obligated
        r"\bpflicht\b",       # German: duty/obligation
        r"\bmüssen\b",         # German: must
    ]
    # Weaker request words
    weak_patterns = [
        r"\bshould\b",
        r"\bare encouraged\b",
        r"\bencourage\b",
        r"\brecommend\b",
        r"\bsollten\b",    # German: should
        r"\bempfehl[ea]n\b",  # German: recommend
        r"\bsoll\b",      # German: shall/should (context ambiguous)
    ]
    # Check for strong and weak patterns
    strong_found = any(re.search(p, t) for p in strong_patterns)
    weak_found = any(re.search(p, t) for p in weak_patterns)
    if strong_found:
        return 2.0
    if weak_found:
        return 1.0
    # Default to request (minimum) if nothing found
    return CONDITION_BOUNDS["C1"][0]


def classify_c2(text: str) -> float:
    """Classify opt‑out provisions (C2).

    -1: Deposit opt‑out allowed and OA opt‑out allowed unconditionally.
     1: No opt‑out allowed (deposit required, OA required).
     2: No deposit opt‑out but unconditional or conditional OA opt‑out.

    The classification attempts to detect these situations from the
    presence or absence of opt‑out/waiver language.  If nothing is
    specified it defaults to 0 (midpoint between −1 and 2).
    """
    t = text.lower()
    # Patterns indicating that authors may choose not to deposit
    deposit_optout_patterns = [
        r"deposit.*\b(opt\-?out|waive)\b",
        r"\bopt\-?out of deposit\b",
        r"\bverzicht auf hinterlegung\b",  # German: opt out of deposit
    ]
    # Patterns indicating an opt‑out for open access but not deposit
    oa_optout_patterns = [
        r"open access.*\bopt\-?out\b",
        r"\bopt\-?out of open access\b",
        r"\bverzicht auf open access\b",
        r"\bembargo.*upon request\b",
    ]
    # Patterns indicating no opt‑out (mandatory deposit & OA)
    no_optout_patterns = [
        r"\bno opt\-?out\b",
        r"\bkeine ausnahme\b",  # German: no exception
        r"\bwithout exception\b",
    ]
    deposit_optout = any(re.search(p, t) for p in deposit_optout_patterns)
    oa_optout = any(re.search(p, t) for p in oa_optout_patterns)
    no_optout = any(re.search(p, t) for p in no_optout_patterns)
    # Determine classification
    if deposit_optout and oa_optout:
        # Both deposit and OA can be waived
        return -1.0
    if no_optout:
        return 1.0
    if not deposit_optout and oa_optout:
        # Deposit required but OA can be opted out
        return 2.0
    # Default to midpoint (0) when unspecified or ambiguous
    return 0.0


def classify_c3(text: str) -> float:
    """Classify which version must be deposited (C3).

    Returns:
      0.8 for explicit mention of the author’s accepted manuscript (AAM)
          or the publisher’s version of record (VoR);
      0.4 for explicit mention of an unrefereed preprint;
      0 for unspecified.
    """
    t = text.lower()
    if re.search(r"(author[^\n]{0,30}version|accepted manuscript|aam|autorenfassung)", t):
        return 0.8
    if re.search(r"(publisher[^\n]{0,30}version|version of record|vor)", t):
        return 0.8
    if re.search(r"preprint", t):
        # Unrefereed preprint (if explicitly mentioned)
        return 0.4
    return 0.0


def classify_c4(text: str) -> float:
    """Classify deposit timing (C4).

    Values:
        2   At time of acceptance (or immediately upon acceptance)
        1.5 At time of publication
        0.5 As soon as possible / promptly
        0   Unspecified or other
    """
    t = text.lower()
    if re.search(r"(time|upon) of acceptance|bei annahme|nach annahme", t):
        return 2.0
    if re.search(r"(at|upon) publication|bei veröffentlichung|nach veröffentlichung", t):
        return 1.5
    if re.search(r"as soon as possible|promptly|so bald wie möglich", t):
        return 0.5
    return 0.0


def classify_c5(text: str) -> float:
    """Classify embargo length (C5).

    Values:
        0.5  6 months after publication
       -2    12 months or more (including unspecified or publisher‑dictated)
    """
    t = text.lower()
    # 6 months embargo
    if re.search(r"(six|6)\\s+months?", t) and re.search(r"(embargo|after publication|nach veröffentlichung)", t):
        return 0.5
    # 12 months or more
    if re.search(r"(twelve|12)\\s+months?|mehr als 12 monate|one year|ein jahr", t):
        return -2.0
    # Generic statements deferring to publisher or unspecified period
    if re.search(r"embargo|period stipulated by the publisher|verlag", t):
        return -2.0
    # Unspecified: treat as worst case (−2)
    return -2.0


def classify_c6(text: str) -> float:
    """Classify copyright reservation (C6).

    Values:
        2:  Blanket rights reservation (non‑exclusive rights retained, licence to publisher, rights retention guidance)
        1:  Opt‑out allowed on case‑by‑case basis / admonition to retain rights / agreements must comply
       -2:  No copyright reservation
        0:  Unspecified
    """
    t = text.lower()
    # Strong rights retention
    strong_patterns = [
        r"retain[\\s\\w]{0,20}non\\-exclusive rights",
        r"grant[\\s\\w]{0,20}non\\-exclusive licence",
        r"license[^\\n]{0,40}right[s]? to publisher",
        r"copyright will be retained",
        r"blanket copyright reservation",
        r"autoren behalten das recht",  # German: authors retain the right
    ]
    # Weaker rights retention / opt‑out possible
    medium_patterns = [
        r"may opt out of rights reservation",
        r"case\\-by\\-case basis",
        r"authors should retain copyright",
        r"authors should retain rights whenever possible",
        r"any agreements must comply",
        r"rechte sollten behalten",  # German: rights should be retained
    ]
    # Explicitly no rights reservation
    negative_patterns = [
        r"no copyright reservation",
        r"copyright is transferred",
        r"copyright assignment",
        r"urheberrecht.*übertragen",  # German: copyright transferred
    ]
    if any(re.search(p, t) for p in strong_patterns):
        return 2.0
    if any(re.search(p, t) for p in medium_patterns):
        return 1.0
    if any(re.search(p, t) for p in negative_patterns):
        return -2.0
    # Unspecified
    return 0.0


def classify_c7(text: str) -> float:
    """Classify internal use requirement (C7).

    Returns 2 if the policy indicates that deposit is required for
    internal purposes such as performance reviews, promotion, or
    evaluation.  Otherwise returns 0.
    """
    t = text.lower()
    patterns = [
        r"performance review",
        r"performance evaluation",
        r"promotion",
        r"tenure",
        r"internal use",
        r"leistungsbewertung",    # German: performance evaluation
        r"evaluationszwecke",     # German: evaluation purposes
    ]
    if any(re.search(p, t) for p in patterns):
        return 2.0
    return 0.0


def classify_c8(text: str) -> float:
    """Classify whether theses/dissertations are covered (C8).

    Returns 2 if the policy explicitly refers to theses or
    dissertations; otherwise returns 0.
    """
    t = text.lower()
    if re.search(r"(thesis|theses|dissertation|doktorarbeit|abschlussarbeit)", t):
        return 2.0
    return 0.0


def normalise(value: float, cond: str) -> float:
    """Normalise a raw value for condition `cond` to the [0, 1] range.

    Values outside the known range are clipped.  The minimum and
    maximum for each condition are defined in CONDITION_BOUNDS.
    """
    min_val, max_val = CONDITION_BOUNDS[cond]
    # Prevent division by zero for degenerate ranges
    if max_val == min_val:
        return 0.0
    # Clip to bounds
    if value < min_val:
        value = min_val
    if value > max_val:
        value = max_val
    return (value - min_val) / (max_val - min_val)


def score_policy(values: Dict[str, float], weights: Dict[str, float]) -> float:
    """Compute a weighted score (0–100) given raw condition values and weights.

    Each raw value is first normalised to [0, 1] using CONDITION_BOUNDS.
    The weighted sum of these normalised values is multiplied by 100
    to express the score as a percentage.
    """
    total = 0.0
    for cond, weight in weights.items():
        # If a value is missing default to the lower bound
        raw_value = values.get(cond, CONDITION_BOUNDS[cond][0])
        norm_val = normalise(raw_value, cond)
        total += weight * norm_val
    return round(total * 100, 2)


def analyse_policy(text: str) -> Dict[str, float]:
    """Return a dictionary of raw condition values for a given policy text."""
    return {
        "C1": classify_c1(text),
        "C2": classify_c2(text),
        "C3": classify_c3(text),
        "C4": classify_c4(text),
        "C5": classify_c5(text),
        "C6": classify_c6(text),
        "C7": classify_c7(text),
        "C8": classify_c8(text),
    }


def main() -> None:
    # Ensure the policies directory exists
    if not POLICIES_DIR.is_dir():
        raise RuntimeError(f"Policies directory not found: {POLICIES_DIR}")

    # Collect result rows
    rows = []
    for file_path in sorted(POLICIES_DIR.glob("*.txt")):
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            print(f"Warning: could not read {file_path.name}: {exc}")
            continue
        values = analyse_policy(content)
        initial_score = score_policy(values, INITIAL_WEIGHTS)
        updated_score = score_policy(values, UPDATED_WEIGHTS)
        row = {
            "policy_file": file_path.name,
            **values,
            "initial_score": initial_score,
            "updated_score": updated_score,
        }
        rows.append(row)

    # Create output directory if necessary
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    # Write CSV
    fieldnames = [
        "policy_file",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "initial_score",
        "updated_score",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Write TSV version for QA validation (tab‑separated).  This file
    # mirrors the CSV content but uses a .tsv extension.  Having a TSV
    # available allows qa/lint_tables.py to discover and validate it
    # automatically when run without arguments.
    output_tsv = OUTPUT_CSV.with_suffix(".tsv")
    with output_tsv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    # Print summary to console
    print(f"Processed {len(rows)} policy files.")
    for row in rows:
        print(
            f"{row['policy_file']}: initial={row['initial_score']:.2f}, updated={row['updated_score']:.2f}"
        )


if __name__ == "__main__":
    main()
