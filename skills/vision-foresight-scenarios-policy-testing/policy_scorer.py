#!/usr/bin/env python3
"""
Deterministic policy score matrix processor for vision-foresight-scenarios-policy-testing.

Prevents LLM re-reasoning for: average computation, classification threshold checks,
ranking, and activation-scenario identification.

PDF source: Glenn & TFG V3.0 19장 Section III "Testing policies" + Section II
"dichotomize strategies between robust and contingent elements"

Usage (from SKILL.md Step 5–6):
  echo '{"scenario_names":["S1","S2","S3"],"policy_scores":{"P1":[2,1,2]}}' | python3 policy_scorer.py
  python3 policy_scorer.py --input matrix.json
  python3 policy_scorer.py --validate-only --input matrix.json
"""

import sys
import json
import argparse
from typing import Dict, List, Tuple, Optional

# ── Classification thresholds (grounded in PDF verbatim) ──────────────────────
# PDF: "produces desirable results in all cases" → strict: all scores ≥ +1
# Practical threshold (SKILL.md): avg ≥ +1.0 AND min ≥ 0
# A score of 0 (neutral) is NOT "desirable" per PDF but is "not harmful".
# Policies with avg ≥ +1 but any cell = 0 are flagged ROBUST* (borderline).
ROBUST_AVG_MIN      = 1.0   # avg score threshold for Robust
ROBUST_STRICT_MIN   = 1     # all cells ≥ +1 → ROBUST (no asterisk)
ROBUST_SOFT_MIN     = 0     # all cells ≥ 0, avg ≥ +1 → ROBUST* (borderline)
REJECT_AVG_MAX      = -0.5  # avg < -0.5 → REJECT
VALID_SCORES        = {-2, -1, 0, 1, 2}


def classify_policy(
    policy_name: str, scores: List[int], scenario_names: List[str]
) -> Dict:
    """
    Deterministically classify one policy.

    Returns dict with keys:
      policy, scores, average, classification, borderline,
      activate_in_scenarios (CONTINGENT only), deactivate_in_scenarios (CONTINGENT only)
    """
    n = len(scores)
    avg = sum(scores) / n
    min_score = min(scores)

    # Strict: all ≥ +1 → ROBUST (no flag)
    if avg >= ROBUST_AVG_MIN and min_score >= ROBUST_STRICT_MIN:
        classification = "ROBUST"
        borderline = False
    # Soft: avg ≥ +1 but some cells = 0 → ROBUST* (borderline)
    elif avg >= ROBUST_AVG_MIN and min_score >= ROBUST_SOFT_MIN:
        classification = "ROBUST"
        borderline = True  # flagged: 0-cell(s) present
    # Reject: avg clearly negative
    elif avg < REJECT_AVG_MAX:
        classification = "REJECT"
        borderline = False
    else:
        classification = "CONTINGENT"
        borderline = False

    result = {
        "policy": policy_name,
        "scores": scores,
        "score_by_scenario": dict(zip(scenario_names, scores)),
        "average": round(avg, 2),
        "min_score": min_score,
        "classification": classification,
        "borderline": borderline,
    }

    if classification == "CONTINGENT":
        favorable = [scenario_names[i] for i, s in enumerate(scores) if s >= 1]
        unfavorable = [scenario_names[i] for i, s in enumerate(scores) if s <= -1]
        result["activate_in_scenarios"] = favorable
        result["deactivate_in_scenarios"] = unfavorable

        # Edge case: CONTINGENT with no favorable scenarios = can never be activated
        # → reclassify as REJECT per PDF "called on IF circumstances develop"
        if not favorable:
            result["classification"] = "REJECT"
            result["note"] = (
                "Reclassified REJECT: avg≥-0.5 but no scenario produces desirable outcome. "
                "PDF requires 'contingent policies that can be CALLED ON if circumstances develop' "
                "— a policy with no favorable scenario cannot be called on."
            )

    if borderline:
        neutral_scenarios = [scenario_names[i] for i, s in enumerate(scores) if s == 0]
        result["neutral_scenarios"] = neutral_scenarios
        result["note"] = (
            "ROBUST* — avg≥+1 but neutral (0) in: "
            + ", ".join(neutral_scenarios)
            + ". PDF verbatim requires 'desirable in ALL cases'. Review needed."
        )

    return result


def process_matrix(
    policy_scores: Dict[str, List[int]], scenario_names: List[str]
) -> Dict:
    """
    Process full policy × scenario matrix.
    Returns structured JSON with classifications, rankings, and leading-indicators handoff.
    """
    classified = []
    for pname, scores in policy_scores.items():
        classified.append(classify_policy(pname, scores, scenario_names))

    # Sort order: ROBUST first (avg desc), CONTINGENT (avg desc), REJECT (avg desc)
    order_map = {"ROBUST": 0, "CONTINGENT": 1, "REJECT": 2}
    classified.sort(key=lambda r: (order_map[r["classification"]], -r["average"]))

    robust     = [r for r in classified if r["classification"] == "ROBUST"]
    contingent = [r for r in classified if r["classification"] == "CONTINGENT"]
    reject     = [r for r in classified if r["classification"] == "REJECT"]

    # Add rank within category
    for rank, r in enumerate(robust, 1):
        r["rank"] = rank
    for rank, r in enumerate(contingent, 1):
        r["rank"] = rank

    # Leading-indicators handoff payload (consumed by next sub-skill)
    leading_indicators_handoff = {
        "contingent_policies": [
            {
                "policy": r["policy"],
                "activate_in_scenarios": r.get("activate_in_scenarios", []),
                "deactivate_in_scenarios": r.get("deactivate_in_scenarios", []),
                "avg_score": r["average"],
            }
            for r in contingent
        ],
        "robust_policies": [
            {"policy": r["policy"], "avg_score": r["average"]}
            for r in robust
        ],
        "scenario_names": scenario_names,
    }

    return {
        "status": "OK",
        "summary": {
            "total_policies": len(classified),
            "scenario_count": len(scenario_names),
            "scenario_names": scenario_names,
            "robust_count": len(robust),
            "robust_borderline_count": sum(1 for r in robust if r["borderline"]),
            "contingent_count": len(contingent),
            "reject_count": len(reject),
        },
        "robust_policies": robust,
        "contingent_policies": contingent,
        "rejected_policies": reject,
        "all_ranked": classified,
        "leading_indicators_handoff": leading_indicators_handoff,
    }


def validate_inputs(
    policy_scores: Dict[str, List[int]], scenario_names: List[str]
) -> List[str]:
    """Returns list of validation errors. Empty list = all OK."""
    errors = []

    if not scenario_names:
        errors.append("scenario_names cannot be empty")
    elif len(scenario_names) < 2:
        errors.append(
            f"Minimum 2 scenarios required for meaningful policy testing "
            f"(got {len(scenario_names)})"
        )

    if not policy_scores:
        errors.append("policy_scores cannot be empty (at least 1 policy required)")

    seen_names = set()
    for pname, scores in policy_scores.items():
        if not pname.strip():
            errors.append("Policy name cannot be empty or whitespace")
        if pname in seen_names:
            errors.append(f"Duplicate policy name: '{pname}'")
        seen_names.add(pname)

        if not scores:
            errors.append(f"Policy '{pname}' has an empty score list")
            continue

        if len(scores) != len(scenario_names):
            errors.append(
                f"Policy '{pname}' has {len(scores)} scores but "
                f"{len(scenario_names)} scenarios are defined"
            )

        for s in scores:
            if s not in VALID_SCORES:
                errors.append(
                    f"Policy '{pname}' contains invalid score {s} "
                    f"(must be one of {sorted(VALID_SCORES)})"
                )

    dup_scenarios = [s for s in scenario_names if scenario_names.count(s) > 1]
    if dup_scenarios:
        errors.append(f"Duplicate scenario names: {list(set(dup_scenarios))}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic policy score matrix processor (TFG V3.0 §19)"
    )
    parser.add_argument("--input", help="JSON file path with policy_scores and scenario_names")
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Only validate inputs, do not compute classification"
    )
    args = parser.parse_args()

    if args.input:
        try:
            with open(args.input) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(json.dumps({"status": "ERROR", "errors": [str(e)]}, ensure_ascii=False))
            sys.exit(1)
    else:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "ERROR", "errors": [f"Invalid JSON: {e}"]},
                             ensure_ascii=False))
            sys.exit(1)

    policy_scores  = data.get("policy_scores", {})
    scenario_names = data.get("scenario_names", [])

    errors = validate_inputs(policy_scores, scenario_names)
    if errors:
        print(json.dumps({"status": "ERROR", "errors": errors}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.validate_only:
        print(json.dumps({"status": "OK", "message": "Input validation passed"},
                         ensure_ascii=False))
        return

    result = process_matrix(policy_scores, scenario_names)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
