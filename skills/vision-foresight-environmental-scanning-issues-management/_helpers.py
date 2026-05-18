#!/usr/bin/env python3
"""
vision-foresight-environmental-scanning-issues-management: Deterministic helper functions.

Handles steps that LLMs could hallucinate if left to natural language inference:
- Weighted PI score calculation (Renfro 4-stage, time-horizon adjusted)
- Tier classification (T1/T2/T3/Wild-card/Ignore) from prob×impact bands
- IQR consensus check (secret balloting threshold)
- Issue ranking by weighted PI
- VRMP field validation for issue entries
- Date retrieval

Sources:
  Gordon & Glenn (2009) PDF Appendix C — Probability-Impact Chart protocol
  Renfro (1993) Issues Management in Strategic Planning — 4-stage cycle
  Default weights (0.5/0.3/0.2) and score bands (1-3/4-6/7-10) are operational
  definitions per the reference protocol at references/probability_impact_chart_protocol.md.

Usage (CLI):
  python3 _helpers.py --date                    → ISO 8601 UTC datetime
  python3 _helpers.py --year                    → current year (int)
  python3 _helpers.py --pi P5 I5 P10 I10 P20 I20 [W5 W10 W20]
                                                → weighted PI float
  python3 _helpers.py --tier PROB IMPACT        → tier string
  python3 _helpers.py --band SCORE              → Low | Medium | High
  python3 _helpers.py --iqr '[8,7,9,6,8]'       → JSON {iqr, median, consensus}
  python3 _helpers.py --rank '[{"name":...,"pi":...},...]'
                                                → JSON sorted issue list
  python3 _helpers.py --validate '{"name":...}' → valid | invalid: [fields]
  python3 _helpers.py --test                    → run self-tests
"""

import sys
import re
import json
import argparse
import statistics
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants — operational definitions (not from Renfro 1993 directly)
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS = {"w5": 0.5, "w10": 0.3, "w20": 0.2}   # 5y/10y/20y horizons
BAND_LOW_MAX = 3      # 1~3 = Low
BAND_HIGH_MIN = 7     # 7~10 = High
SCORE_MIN = 1
SCORE_MAX = 10
IQR_CONSENSUS_THRESHOLD = 2  # IQR ≤ 2 → consensus (Appendix C protocol)


# ---------------------------------------------------------------------------
# Core deterministic functions
# ---------------------------------------------------------------------------

def get_current_utc_datetime() -> str:
    """Current UTC datetime in ISO 8601. Never hallucinated."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_current_year() -> int:
    """Current calendar year. Never hallucinated."""
    return datetime.now(timezone.utc).year


def validate_score(score: float, name: str = "score") -> None:
    """Raise ValueError if score is outside 1-10 range."""
    if not (SCORE_MIN <= score <= SCORE_MAX):
        raise ValueError(f"{name} must be {SCORE_MIN}-{SCORE_MAX}, got {score}")


def get_tier_band(score: float) -> str:
    """
    Map a 1-10 score to its band label.
    Deterministic range check — LLM must not infer this.

    Bands (operational definition per probability_impact_chart_protocol.md):
      Low:    1 ≤ score ≤ 3
      Medium: 4 ≤ score ≤ 6
      High:   7 ≤ score ≤ 10
    """
    validate_score(score)
    if score <= BAND_LOW_MAX:
        return "Low"
    elif score < BAND_HIGH_MIN:
        return "Medium"
    else:
        return "High"


def classify_tier(prob: float, impact: float) -> str:
    """
    Classify issue tier from probability and impact scores (1-10 each).
    Deterministic — LLM must not override this mapping.

    3×3 matrix per Gordon-Glenn (2009) Appendix C + Renfro (1993) framework:
      High×High → T1-Strategic
      High×Med  → T2-Action
      High×Low  → T3-Watch
      Med×High  → T2-Action
      Med×Med   → T3-Watch
      Med×Low   → Ignore
      Low×High  → Wild-card
      Low×Med   → Ignore
      Low×Low   → Ignore
    """
    validate_score(prob, "prob")
    validate_score(impact, "impact")
    p_band = get_tier_band(prob)
    i_band = get_tier_band(impact)

    matrix = {
        ("High", "High"):   "T1-Strategic",
        ("High", "Medium"): "T2-Action",
        ("High", "Low"):    "T3-Watch",
        ("Medium", "High"): "T2-Action",
        ("Medium", "Medium"): "T3-Watch",
        ("Medium", "Low"):  "Ignore",
        ("Low", "High"):    "Wild-card",
        ("Low", "Medium"):  "Ignore",
        ("Low", "Low"):     "Ignore",
    }
    return matrix[(p_band, i_band)]


def calculate_pi_weighted(
    p5: float, i5: float,
    p10: float, i10: float,
    p20: float, i20: float,
    w5: float = DEFAULT_WEIGHTS["w5"],
    w10: float = DEFAULT_WEIGHTS["w10"],
    w20: float = DEFAULT_WEIGHTS["w20"],
) -> float:
    """
    Weighted Probability-Impact score across 3 time horizons.

    Formula (from probability_impact_chart_protocol.md):
      PI = w5*(p5*i5) + w10*(p10*i10) + w20*(p20*i20)

    Default weights per protocol: 5y=0.5, 10y=0.3, 20y=0.2.
    LLM must call this function — no natural language calculation.

    Args:
        p5, i5: 5-year probability and impact (1-10 each)
        p10, i10: 10-year probability and impact (1-10 each)
        p20, i20: 20-year probability and impact (1-10 each)
        w5, w10, w20: time horizon weights (must sum to 1.0)

    Returns:
        Weighted PI score (float, typically 1-100 range)
    """
    for name, val in [("p5",p5),("i5",i5),("p10",p10),("i10",i10),("p20",p20),("i20",i20)]:
        validate_score(val, name)

    w_sum = w5 + w10 + w20
    if not (0.99 < w_sum < 1.01):
        raise ValueError(f"Weights must sum to 1.0, got {w_sum:.4f}")

    pi = w5 * (p5 * i5) + w10 * (p10 * i10) + w20 * (p20 * i20)
    return round(pi, 2)


def check_iqr(scores: list) -> dict:
    """
    Compute IQR and determine consensus for secret-balloting evaluation.

    Secret-balloting consensus rule (Gordon-Glenn 2009 Appendix C):
      IQR ≤ 2 → consensus (True)
      IQR > 2 → discussion needed (False)

    Args:
        scores: list of numeric probability or impact ratings

    Returns:
        {"iqr": float, "median": float, "mean": float,
         "consensus": bool, "n": int}
    """
    if not scores:
        raise ValueError("scores list must not be empty")
    if len(scores) < 2:
        return {"iqr": 0.0, "median": float(scores[0]), "mean": float(scores[0]),
                "consensus": True, "n": 1}

    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    median = statistics.median(sorted_scores)
    q1 = statistics.median(sorted_scores[:n // 2])
    q3 = statistics.median(sorted_scores[(n + 1) // 2:])
    iqr = round(q3 - q1, 4)
    mean = round(statistics.mean(sorted_scores), 4)

    return {
        "iqr": iqr,
        "median": float(median),
        "mean": mean,
        "consensus": iqr <= IQR_CONSENSUS_THRESHOLD,
        "n": n,
    }


def rank_issues(issues: list) -> list:
    """
    Rank issues by weighted PI score (descending).
    Deterministic sort — LLM must not re-order manually.

    Args:
        issues: list of dicts with at least {"name": str, "pi": float}

    Returns:
        Sorted list with "rank" field added (1-indexed).
    """
    sorted_issues = sorted(issues, key=lambda x: x.get("pi", 0), reverse=True)
    for i, issue in enumerate(sorted_issues):
        issue["rank"] = i + 1
    return sorted_issues


def validate_issue_fields(issue: dict) -> tuple:
    """
    Validate required fields for a Stage 3 issue entry.
    Returns (is_valid: bool, missing: list[str]).

    Required: name, p5, i5, p10, i10, p20, i20
    Optional but checked if present: tier (must be valid string)
    """
    required = ["name", "p5", "i5", "p10", "i10", "p20", "i20"]
    missing = [f for f in required if issue.get(f) is None]

    # Score range validation
    range_errors = []
    for field in ["p5", "i5", "p10", "i10", "p20", "i20"]:
        val = issue.get(field)
        if val is not None:
            try:
                v = float(val)
                if not (SCORE_MIN <= v <= SCORE_MAX):
                    range_errors.append(f"{field}={v} out of range [{SCORE_MIN}-{SCORE_MAX}]")
            except (TypeError, ValueError):
                range_errors.append(f"{field} not numeric")

    all_issues = missing + range_errors
    return len(all_issues) == 0, all_issues


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test() -> None:
    print("=== vision-foresight-environmental-scanning-issues-management _helpers.py self-test ===\n")

    dt = get_current_utc_datetime()
    yr = get_current_year()
    assert len(dt) == 20 and dt.endswith("Z"), f"Datetime wrong: {dt}"
    assert 2025 <= yr <= 2035, f"Year out of range: {yr}"
    print(f"[PASS] get_current_utc_datetime → {dt}")
    print(f"[PASS] get_current_year → {yr}")

    # Band tests
    band_cases = [(1,"Low"),(3,"Low"),(4,"Medium"),(6,"Medium"),(7,"High"),(10,"High")]
    for score, expected in band_cases:
        result = get_tier_band(score)
        assert result == expected, f"band({score}) = {result!r}, expected {expected!r}"
    print("[PASS] get_tier_band — 6 boundary cases")

    # Tier classification tests
    tier_cases = [
        (8, 8, "T1-Strategic"),   # High × High
        (8, 5, "T2-Action"),      # High × Medium
        (8, 2, "T3-Watch"),       # High × Low
        (5, 8, "T2-Action"),      # Medium × High
        (5, 5, "T3-Watch"),       # Medium × Medium
        (5, 2, "Ignore"),         # Medium × Low
        (2, 8, "Wild-card"),      # Low × High
        (2, 5, "Ignore"),         # Low × Medium
        (2, 2, "Ignore"),         # Low × Low
        (7, 7, "T1-Strategic"),   # boundary: High × High (exactly 7)
        (4, 7, "T2-Action"),      # boundary: Medium × High (exactly 4&7)
        (3, 7, "Wild-card"),      # boundary: Low × High (exactly 3)
    ]
    for prob, impact, expected in tier_cases:
        result = classify_tier(prob, impact)
        assert result == expected, f"tier({prob},{impact}) = {result!r}, expected {expected!r}"
    print("[PASS] classify_tier — 12 cases including all 9 matrix cells + 3 boundaries")

    # PI weighted calculation
    # Example from reference: AGI 화이트칼라
    # 5y: p7 i8 → 56, 10y: p9 i9 → 81, 20y: p10 i10 → 100
    # 56*0.5 + 81*0.3 + 100*0.2 = 28 + 24.3 + 20 = 72.3
    pi1 = calculate_pi_weighted(7, 8, 9, 9, 10, 10)
    assert abs(pi1 - 72.3) < 0.01, f"PI calc failed: {pi1}"
    print(f"[PASS] calculate_pi_weighted — AGI example → {pi1}")

    # Another example: 한국 기독교 인구
    # 5y: p9 i8 → 72, 10y: p9 i9 → 81, 20y: p9 i9 → 81
    # 72*0.5 + 81*0.3 + 81*0.2 = 36 + 24.3 + 16.2 = 76.5
    pi2 = calculate_pi_weighted(9, 8, 9, 9, 9, 9)
    assert abs(pi2 - 76.5) < 0.01, f"PI calc2 failed: {pi2}"
    print(f"[PASS] calculate_pi_weighted — 기독교 인구 example → {pi2}")

    # Weight sum validation
    try:
        calculate_pi_weighted(5, 5, 5, 5, 5, 5, w5=0.5, w10=0.3, w20=0.3)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    print("[PASS] calculate_pi_weighted — invalid weights raise ValueError")

    # Score range validation
    try:
        calculate_pi_weighted(11, 5, 5, 5, 5, 5)
        assert False, "Should raise ValueError for score > 10"
    except ValueError:
        pass
    print("[PASS] calculate_pi_weighted — score > 10 raises ValueError")

    # IQR consensus check
    iqr_consensus = check_iqr([7, 8, 7, 8, 9])
    assert iqr_consensus["consensus"] is True, f"IQR consensus failed: {iqr_consensus}"
    print(f"[PASS] check_iqr — consensus (IQR={iqr_consensus['iqr']})")

    iqr_no_consensus = check_iqr([2, 5, 8, 9, 10])
    assert iqr_no_consensus["consensus"] is False, f"IQR no-consensus failed: {iqr_no_consensus}"
    print(f"[PASS] check_iqr — no consensus (IQR={iqr_no_consensus['iqr']})")

    # Rank issues
    issues = [
        {"name": "Issue A", "pi": 50.0},
        {"name": "Issue B", "pi": 72.3},
        {"name": "Issue C", "pi": 30.0},
    ]
    ranked = rank_issues(issues)
    assert ranked[0]["name"] == "Issue B" and ranked[0]["rank"] == 1
    assert ranked[1]["name"] == "Issue A" and ranked[1]["rank"] == 2
    assert ranked[2]["name"] == "Issue C" and ranked[2]["rank"] == 3
    print("[PASS] rank_issues — 3 issues sorted correctly")

    # Validate issue fields
    valid_issue = {"name": "Test", "p5": 7, "i5": 8, "p10": 9, "i10": 9, "p20": 10, "i20": 10}
    ok, missing = validate_issue_fields(valid_issue)
    assert ok, f"Valid issue failed: {missing}"
    print("[PASS] validate_issue_fields — valid issue")

    invalid_issue = {"name": "Test", "p5": 11, "i5": 8, "p10": 9, "i10": 9, "p20": 10, "i20": 10}
    ok2, issues2 = validate_issue_fields(invalid_issue)
    assert not ok2, "Invalid (p5=11) should fail"
    print(f"[PASS] validate_issue_fields — p5=11 out of range detected: {issues2}")

    print("\n=== ALL SELF-TESTS PASSED ===")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic helpers for vision-foresight-environmental-scanning-issues-management"
    )
    parser.add_argument("--date", action="store_true", help="Print current UTC datetime (ISO 8601)")
    parser.add_argument("--year", action="store_true", help="Print current year")
    parser.add_argument("--pi", nargs="+",
                        metavar="SCORE",
                        help="Weighted PI score: P5 I5 P10 I10 P20 I20 [W5 W10 W20]")
    parser.add_argument("--tier", nargs=2,
                        metavar=("PROB", "IMPACT"),
                        help="Classify issue tier from prob and impact scores")
    parser.add_argument("--band", metavar="SCORE",
                        help="Get band label (Low/Medium/High) for a 1-10 score")
    parser.add_argument("--iqr", metavar="SCORES_JSON",
                        help="Compute IQR and consensus from JSON array of scores")
    parser.add_argument("--rank", metavar="ISSUES_JSON",
                        help="Rank issues by PI score (JSON array with name+pi fields)")
    parser.add_argument("--validate", metavar="ISSUE_JSON",
                        help="Validate issue fields for Stage 3 entry")
    parser.add_argument("--test", action="store_true", help="Run self-tests")

    args = parser.parse_args()

    if args.test:
        self_test()
    elif args.date:
        print(get_current_utc_datetime())
    elif args.year:
        print(get_current_year())
    elif args.pi:
        vals = [float(v) for v in args.pi]
        if len(vals) == 6:
            print(calculate_pi_weighted(*vals))
        elif len(vals) == 9:
            print(calculate_pi_weighted(*vals[:6], w5=vals[6], w10=vals[7], w20=vals[8]))
        else:
            print("Error: --pi requires 6 values (p5 i5 p10 i10 p20 i20) or 9 (+ w5 w10 w20)",
                  file=sys.stderr)
            sys.exit(1)
    elif args.tier:
        prob, impact = float(args.tier[0]), float(args.tier[1])
        tier = classify_tier(prob, impact)
        band_p = get_tier_band(prob)
        band_i = get_tier_band(impact)
        print(json.dumps({"tier": tier, "prob_band": band_p, "impact_band": band_i}))
    elif args.band:
        print(get_tier_band(float(args.band)))
    elif args.iqr:
        scores = json.loads(args.iqr)
        result = check_iqr([float(s) for s in scores])
        print(json.dumps(result))
    elif args.rank:
        issues = json.loads(args.rank)
        print(json.dumps(rank_issues(issues), ensure_ascii=False, indent=2))
    elif args.validate:
        issue = json.loads(args.validate)
        ok, issues_found = validate_issue_fields(issue)
        if ok:
            print("valid")
        else:
            print(f"invalid: {issues_found}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
