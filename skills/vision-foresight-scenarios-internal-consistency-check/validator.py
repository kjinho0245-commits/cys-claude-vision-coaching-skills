#!/usr/bin/env python3
"""
vision-foresight-scenarios-internal-consistency-check — Deterministic Validator
결정론적 검증기: LLM이 자연어로 재추론하지 못하는 항목을 Python으로 강제 검증.

Usage:
  python3 validator.py --input audit_data.json
  python3 validator.py --demo   # runs self-test with example data

Exit codes: 0=all valid, 1=errors found, 2=warnings only
"""

import json
import sys
import argparse
from typing import Any, Dict, List, Tuple

# ── 1. Score range check ──────────────────────────────────────────────────────

def validate_score(score: Any, label: str) -> Tuple[bool, str]:
    """Score MUST be an integer in [1, 5]. No float, no string, no None."""
    if not isinstance(score, int) or isinstance(score, bool):
        return False, f"SCORE_TYPE_ERROR: {label}={score!r} — must be int, got {type(score).__name__}"
    if score < 1 or score > 5:
        return False, f"SCORE_RANGE_ERROR: {label}={score} — must be 1..5"
    return True, ""


# ── 2. Scenario count check ───────────────────────────────────────────────────

def check_scenario_count(n: int) -> Tuple[str, str]:
    """
    TFG V3.0 Ch19 recommends 4-5 scenarios.
    n < 1  → ERROR (nothing to audit)
    n == 1 → ERROR (cross-scenario comparison structurally impossible)
    n < 4  → WARN
    n > 5  → WARN
    4 ≤ n ≤ 5 → OK
    """
    if n < 1:
        return "ERROR", "No scenarios provided — cannot perform audit"
    if n == 1:
        return "ERROR", (
            "n=1: cross-scenario Internal Consistency check is structurally impossible "
            "(TFG V3.0 Ch19 Section II: 'alternative scenarios should address similar "
            "issues so that they can be compared' — requires ≥2 scenarios)"
        )
    if n < 4:
        return "WARN", (
            f"n={n}: TFG V3.0 Ch19 recommends 4-5 scenarios for robust comparison. "
            f"Cross-scenario audit proceeds but set may be under-differentiated."
        )
    if n > 5:
        return "WARN", (
            f"n={n}: TFG V3.0 Ch19 recommends 4-5 scenarios maximum for manageability. "
            f"Audit proceeds but cognitive load and comparison complexity are elevated."
        )
    return "OK", f"n={n} scenarios: within TFG V3.0 recommended range (4-5)"


# ── 3. Per-scenario Pass/Fail computation ────────────────────────────────────

def compute_scenario_pass_fail(
    plaus: int, consist: int, interest: int
) -> Tuple[str, List[str]]:
    """
    PASS condition (SKILL.md §4 Step 6):
      All three criteria ≥ 3 per scenario.
    Returns (PASS|FAIL, list_of_failure_reasons).
    """
    failures = []
    if plaus < 3:
        failures.append(f"Plausibility={plaus} < 3 (threshold)")
    if consist < 3:
        failures.append(f"InternalConsistency={consist} < 3 (threshold)")
    if interest < 3:
        failures.append(f"Interest={interest} < 3 (threshold)")
    return ("PASS" if not failures else "FAIL"), failures


# ── 4. Cross-scenario consistency pass/fail ──────────────────────────────────

def compute_cross_pass_fail(cross_score: int) -> Tuple[str, List[str]]:
    """Cross-scenario consistency ≥ 3 required (SKILL.md §4 Step 6)."""
    if cross_score < 3:
        return "FAIL", [f"CrossScenarioConsistency={cross_score} < 3 (threshold)"]
    return "PASS", []


# ── 5. Required-section presence check ───────────────────────────────────────

REQUIRED_TOP_KEYS = {
    "scenarios",
    "cross_scenario_consistency",
    "section_iv_flags",
    "overall_pass_fail",
}

REQUIRED_SCENARIO_KEYS = {
    "id",
    "plausibility",
    "internal_consistency",
    "interest",
    "pass_fail",
}

REQUIRED_FLAG_KEYS = {
    "writer_mental_model_bias",
    "controversial_items_omitted",
    "conventional_wisdom_bias",
}


def check_required_sections(audit: Dict) -> List[str]:
    errors = []
    for key in REQUIRED_TOP_KEYS:
        if key not in audit:
            errors.append(f"MISSING_SECTION: top-level key '{key}' absent")
    if "scenarios" in audit:
        for i, s in enumerate(audit["scenarios"]):
            for k in REQUIRED_SCENARIO_KEYS:
                if k not in s:
                    errors.append(f"MISSING_FIELD: scenario[{i}] missing '{k}'")
    if "section_iv_flags" in audit:
        flags = audit["section_iv_flags"]
        if not isinstance(flags, dict):
            errors.append("TYPE_ERROR: section_iv_flags must be a JSON object")
        else:
            for k in REQUIRED_FLAG_KEYS:
                if k not in flags:
                    errors.append(f"MISSING_FLAG: section_iv_flags missing '{k}'")
    return errors


# ── 6. Pass/Fail declared-vs-computed consistency check ──────────────────────

def check_pass_fail_consistency(audit: Dict) -> List[str]:
    """
    Verify that:
      a) Each scenario's declared pass_fail matches the computed value.
      b) The overall_pass_fail matches the conjunction of all scenario pass/fails
         AND the cross-scenario consistency.
    """
    errors = []
    scenarios = audit.get("scenarios", [])

    computed_overall = "PASS"

    for i, s in enumerate(scenarios):
        label = f"Scenario[{i+1}]"
        plaus = s.get("plausibility")
        consist = s.get("internal_consistency")
        interest = s.get("interest")

        # Only check if scores are valid ints
        if all(isinstance(x, int) and not isinstance(x, bool) for x in [plaus, consist, interest]):
            computed_pf, failures = compute_scenario_pass_fail(plaus, consist, interest)
            declared_pf = s.get("pass_fail")
            if declared_pf and declared_pf != computed_pf:
                errors.append(
                    f"PASS_FAIL_MISMATCH: {label} declared={declared_pf!r} "
                    f"but computed={computed_pf!r}. "
                    f"Failures: {failures if failures else 'none'}"
                )
            if computed_pf == "FAIL":
                computed_overall = "FAIL"

    cross = audit.get("cross_scenario_consistency")
    if isinstance(cross, int) and not isinstance(cross, bool):
        cross_pf, cross_failures = compute_cross_pass_fail(cross)
        if cross_pf == "FAIL":
            computed_overall = "FAIL"

    declared_overall = audit.get("overall_pass_fail")
    if declared_overall and declared_overall != computed_overall:
        errors.append(
            f"OVERALL_MISMATCH: declared overall_pass_fail={declared_overall!r} "
            f"but computed={computed_overall!r}"
        )

    return errors


# ── 7. Main validation orchestrator ─────────────────────────────────────────

def validate_audit_output(audit: Dict) -> Dict:
    """
    Run all deterministic checks on the LLM-generated audit JSON.
    Returns:
      {
        "valid": bool,
        "computed_overall_pass_fail": str,
        "errors": [str, ...],
        "warnings": [str, ...]
      }
    """
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Required sections
    errors.extend(check_required_sections(audit))

    scenarios = audit.get("scenarios", [])
    if not isinstance(scenarios, list):
        errors.append("TYPE_ERROR: 'scenarios' must be a JSON array")
        scenarios = []

    # 2. Scenario count
    n = len(scenarios)
    count_status, count_msg = check_scenario_count(n)
    if count_status == "ERROR":
        errors.append(f"COUNT_ERROR: {count_msg}")
    elif count_status == "WARN":
        warnings.append(f"COUNT_WARN: {count_msg}")

    # 3. Per-scenario score range
    for i, s in enumerate(scenarios):
        label_base = f"Scenario[{i+1}]"
        for criterion in ("plausibility", "internal_consistency", "interest"):
            score = s.get(criterion)
            ok, msg = validate_score(score, f"{label_base}.{criterion}")
            if not ok:
                errors.append(msg)

    # 4. Cross-scenario score range
    cross = audit.get("cross_scenario_consistency")
    if cross is not None:
        ok, msg = validate_score(cross, "cross_scenario_consistency")
        if not ok:
            errors.append(msg)

    # 5. Pass/Fail consistency (only if scores are valid)
    errors.extend(check_pass_fail_consistency(audit))

    # 6. Section IV flags type check
    flags = audit.get("section_iv_flags", {})
    if isinstance(flags, dict):
        for k, v in flags.items():
            if not isinstance(v, bool):
                errors.append(
                    f"TYPE_ERROR: section_iv_flags.{k}={v!r} must be boolean"
                )

    # Compute overall
    computed_overall = "PASS"
    for s in scenarios:
        plaus = s.get("plausibility")
        consist = s.get("internal_consistency")
        interest = s.get("interest")
        if all(isinstance(x, int) and not isinstance(x, bool) for x in [plaus, consist, interest]):
            pf, _ = compute_scenario_pass_fail(plaus, consist, interest)
            if pf == "FAIL":
                computed_overall = "FAIL"
    if isinstance(cross, int) and not isinstance(cross, bool):
        cross_pf, _ = compute_cross_pass_fail(cross)
        if cross_pf == "FAIL":
            computed_overall = "FAIL"

    return {
        "valid": len(errors) == 0,
        "computed_overall_pass_fail": computed_overall,
        "errors": errors,
        "warnings": warnings,
    }


# ── 8. Demo / self-test ───────────────────────────────────────────────────────

DEMO_VALID = {
    "scenarios": [
        {"id": 1, "plausibility": 4, "internal_consistency": 5, "interest": 4, "pass_fail": "PASS"},
        {"id": 2, "plausibility": 3, "internal_consistency": 4, "interest": 5, "pass_fail": "PASS"},
        {"id": 3, "plausibility": 2, "internal_consistency": 3, "interest": 4, "pass_fail": "FAIL"},
        {"id": 4, "plausibility": 4, "internal_consistency": 4, "interest": 3, "pass_fail": "PASS"},
    ],
    "cross_scenario_consistency": 4,
    "section_iv_flags": {
        "writer_mental_model_bias": False,
        "controversial_items_omitted": False,
        "conventional_wisdom_bias": True,
    },
    "overall_pass_fail": "FAIL",
}

DEMO_INVALID = {
    "scenarios": [
        {"id": 1, "plausibility": 6, "internal_consistency": 3, "interest": 4, "pass_fail": "PASS"},
        {"id": 2, "plausibility": 3, "internal_consistency": 3, "interest": 3, "pass_fail": "FAIL"},
    ],
    "cross_scenario_consistency": 3,
    "section_iv_flags": {
        "writer_mental_model_bias": "yes",
        "controversial_items_omitted": False,
        "conventional_wisdom_bias": False,
    },
    "overall_pass_fail": "PASS",
}


def run_demo():
    print("=== DEMO: Valid audit (one scenario fails plausibility) ===")
    r = validate_audit_output(DEMO_VALID)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()
    print("=== DEMO: Invalid audit (score=6, bool mismatch, type error) ===")
    r2 = validate_audit_output(DEMO_INVALID)
    print(json.dumps(r2, ensure_ascii=False, indent=2))


# ── 9. CLI entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic validator for vision-foresight-scenarios-internal-consistency-check audit JSON"
    )
    parser.add_argument("--input", help="Path to audit JSON file")
    parser.add_argument("--demo", action="store_true", help="Run self-test with demo data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(2)

    with open(args.input, encoding="utf-8") as f:
        audit_data = json.load(f)

    result = validate_audit_output(audit_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["valid"]:
        sys.exit(1)
    elif result["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)
