#!/usr/bin/env python3
"""
vision-foresight-scenarios-scenario-logics-selection — Deterministic Helper
======================================================================
결정론적 헬퍼: 2^n 조합 생성, 선택 카운트 검증, 축 레이블 포맷.
LLM이 자연어로 재추론하지 못하는 항목을 Python으로 처리.

사용법:
  python3 scenario_logics_helper.py generate_combinations <n>
  python3 scenario_logics_helper.py validate_selection <n_mathematical> <n_excluded> <n_selected> [--mode default|defense_markets]
  python3 scenario_logics_helper.py generate_space '<axes_json>'
  python3 scenario_logics_helper.py format_matrix '<axes_json>' '<scenarios_json>'
  python3 scenario_logics_helper.py exclusion_rules
  python3 scenario_logics_helper.py demo

Exit codes: 0=pass, 1=fail/error
"""

import json
import sys
import itertools
import argparse
from typing import Any, Dict, List, Optional, Tuple


# ── 1. 조합 생성 (Combination Generator) ─────────────────────────────────────

def generate_combinations(n_axes: int) -> Dict[str, Any]:
    """
    Deterministically generate all 2^n binary combinations for n axes.
    0 = Low, 1 = High for each axis.

    MITRE default: n=2 → 4 combinations (quadrants)
    Defense Markets Thor: n=4 → 16 combinations (TFG verbatim)
    """
    if n_axes < 2:
        return {
            "valid": False,
            "error": f"n_axes must be >= 2, got {n_axes}. Minimum 2 axes required."
        }
    if n_axes > 6:
        return {
            "valid": False,
            "error": (
                f"n_axes={n_axes} → 2^{n_axes}={2**n_axes} combinations. "
                "Hard limit: Use foresight-morphological-analysis cross-skill for n_axes > 6."
            )
        }

    warnings = []
    if n_axes > 4:
        warnings.append(
            f"COMPLEXITY_WARN: n_axes={n_axes} → 2^{n_axes}={2**n_axes} combinations. "
            "Recommended to use foresight-morphological-analysis cross-skill for n > 4. "
            "Proceeding with computation."
        )

    combos = list(itertools.product([0, 1], repeat=n_axes))
    total = len(combos)  # Always exactly 2^n

    labeled = []
    for idx, combo in enumerate(combos, 1):
        state_labels = ["High" if s == 1 else "Low" for s in combo]
        axis_labels = [f"A{j + 1}:{state_labels[j]}" for j in range(n_axes)]
        labeled.append({
            "id": idx,
            "binary": list(combo),
            "state_labels": state_labels,
            "label": " + ".join(axis_labels)
        })

    result = {
        "valid": True,
        "n_axes": n_axes,
        "mathematical_total": total,
        "formula": f"2^{n_axes} = {total}",
        "combinations": labeled
    }
    if warnings:
        result["warnings"] = warnings
    return result


# ── 2. 선택 카운트 검증 (Selection Count Validator) ──────────────────────────

def validate_selection(n_mathematical: int, n_excluded: int, n_selected: int,
                       mode: str = "default") -> Dict[str, Any]:
    """
    Validate scenario selection counts against PDF rules.

    PDF verbatim: "Four to five 'worlds' seems ideal to capture a range
    of future challenges and opportunities."

    Defense Markets exception: 4-axis → 16 math → 13 plausible → 6 selected
    (n_selected=6 is allowed for defense_markets mode only)

    Args:
        n_mathematical: total combinations (must equal 2^n_axes)
        n_excluded:     excluded as implausible
        n_selected:     final worlds chosen
        mode:           "default" (4-5) | "defense_markets" (4-6 for 4-axis)
    """
    errors: List[str] = []
    warnings: List[str] = []

    # Input range validation
    if n_mathematical <= 0:
        return {
            "valid": False,
            "errors": [f"INPUT_ERROR: n_mathematical={n_mathematical} must be > 0"],
            "warnings": [],
            "summary": "FAIL"
        }
    if n_excluded < 0:
        return {
            "valid": False,
            "errors": [f"INPUT_ERROR: n_excluded={n_excluded} must be >= 0"],
            "warnings": [],
            "summary": "FAIL"
        }
    if n_selected <= 0:
        return {
            "valid": False,
            "errors": [f"INPUT_ERROR: n_selected={n_selected} must be > 0"],
            "warnings": [],
            "summary": "FAIL"
        }

    # Compute n_plausible deterministically
    n_plausible = n_mathematical - n_excluded

    if n_plausible <= 0:
        errors.append(
            f"PLAUSIBLE_ERROR: n_plausible={n_plausible} <= 0. "
            f"Cannot exclude {n_excluded} from {n_mathematical}. Review exclusion criteria."
        )

    if n_plausible < n_selected:
        errors.append(
            f"SELECTION_IMPOSSIBLE: Cannot select {n_selected} worlds from only "
            f"{n_plausible} plausible (total={n_mathematical}, excluded={n_excluded})"
        )

    # Selection count range rule
    if mode == "defense_markets":
        min_select, max_select = 4, 6
        rule_source = "Defense Markets Thor 양식 (4-axis): 4-6 worlds allowed"
    else:
        min_select, max_select = 4, 5
        rule_source = 'PDF verbatim: "Four to five worlds seems ideal"'

    if n_selected < min_select:
        errors.append(
            f"COUNT_FAIL: n_selected={n_selected} < {min_select} minimum. "
            f"Rule: {rule_source}"
        )
    elif n_selected > max_select:
        errors.append(
            f"COUNT_FAIL: n_selected={n_selected} > {max_select} maximum. "
            f"Rule: {rule_source}"
        )

    # Warn if 2-axis has more than 1 exclusion
    if n_mathematical == 4 and n_excluded > 1:
        warnings.append(
            f"EXCLUSION_WARN: Excluding {n_excluded} from 4 quadrants (2-axis). "
            "For 2-axis analysis, all 4 quadrants are typically plausible. "
            "Verify exclusion rationale strictly."
        )

    # Warn if all 2-axis quadrants are excluded
    if n_mathematical == 4 and n_excluded >= 4:
        errors.append(
            "AXIS_ERROR: All 4 quadrants excluded — axis selection itself may be invalid. "
            "Reconsider axis choice or endpoint definitions."
        )

    return {
        "valid": len(errors) == 0,
        "n_mathematical": n_mathematical,
        "n_excluded": n_excluded,
        "n_plausible": n_plausible,
        "n_selected": n_selected,
        "mode": mode,
        "errors": errors,
        "warnings": warnings,
        "summary": "PASS" if len(errors) == 0 else "FAIL"
    }


# ── 3. 전체 시나리오 공간 생성 (Full Scenario Space Generator) ────────────────

def generate_space(axes: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Generate full scenario space from axes definitions.

    Args:
        axes: List of dicts with required keys: 'name', 'driving_force', 'low', 'high'

    Returns:
        Full scenario space with labeled combinations.
    """
    n = len(axes)

    # Validate axes structure
    required_keys = {"name", "driving_force", "low", "high"}
    for i, axis in enumerate(axes):
        missing = required_keys - set(axis.keys())
        if missing:
            return {
                "valid": False,
                "error": f"Axis {i + 1} missing required keys: {sorted(missing)}"
            }

    # Check duplicate axis names (structural deduplication check)
    names = [a["name"].lower().strip() for a in axes]
    if len(set(names)) != len(names):
        return {
            "valid": False,
            "error": f"Duplicate axis names detected: {names}. Each axis must be distinct."
        }

    # Generate combinations
    combo_result = generate_combinations(n)
    if not combo_result.get("valid"):
        return combo_result

    # Label each combination with axis-specific endpoint names
    labeled = []
    for combo in combo_result["combinations"]:
        label_parts = []
        for j, state in enumerate(combo["binary"]):
            axis = axes[j]
            endpoint = axis["high"] if state == 1 else axis["low"]
            label_parts.append(f"{axis['name']}:{endpoint}")
        labeled.append({
            "id": combo["id"],
            "binary": combo["binary"],
            "state_labels": combo["state_labels"],
            "axis_labels": label_parts,
            "label": " | ".join(label_parts),
            "plausible": None  # Determined by LLM analyst using 3 exclusion rules
        })

    return {
        "valid": True,
        "n_axes": n,
        "mathematical_total": combo_result["mathematical_total"],
        "formula": combo_result["formula"],
        "axes": axes,
        "combinations": labeled
    }


# ── 4. 2-axis MITRE 매트릭스 포맷터 ──────────────────────────────────────────

def format_2axis_matrix(axes: List[Dict], scenarios: List[Dict]) -> str:
    """
    Generate 2-axis MITRE-style markdown table.
    Only valid for exactly 2 axes.

    scenarios: list of dicts with 'binary' ([b1, b2]) and 'name' keys.
    """
    if len(axes) != 2:
        return f"ERROR: 2-axis matrix requires exactly 2 axes, got {len(axes)}"

    a1 = axes[0]
    a2 = axes[1]

    # Build lookup: (b1, b2) → scenario name
    lookup: Dict[Tuple[int, int], str] = {}
    for s in scenarios:
        if "binary" in s and len(s["binary"]) >= 2 and "name" in s:
            key = (int(s["binary"][0]), int(s["binary"][1]))
            lookup[key] = s["name"]

    def cell(b1: int, b2: int) -> str:
        return lookup.get((b1, b2), "—")

    rows = [
        f"|  | **{a2['name']}: {a2['low']}** | **{a2['name']}: {a2['high']}** |",
        "|---|---|---|",
        f"| **{a1['name']}: {a1['high']}** | {cell(1, 0)} | {cell(1, 1)} |",
        f"| **{a1['name']}: {a1['low']}** | {cell(0, 0)} | {cell(0, 1)} |"
    ]
    return "\n".join(rows)


# ── 5. 제외 기준 설명기 ───────────────────────────────────────────────────────

def describe_exclusion_rules() -> str:
    """Return the 3 exclusion rules as a formatted reference string."""
    return """PLAUSIBILITY EXCLUSION RULES (3 Rules — Deterministic Criteria):

Rule 1: INTERNAL CONTRADICTION
  Condition: Two axes states are causally mutually exclusive within the scenario logic.
  Enforcement: LLM MUST provide explicit causal mechanism explanation.
  Example: "Very high AI regulation + Maximum AI capability diffusion"
           (strict regulation structurally prevents rapid capability diffusion)

Rule 2: TEMPORAL IMPOSSIBILITY
  Condition: Combination requires transition faster than planning horizon allows.
  Enforcement: LLM MUST cite specific transition speed constraint or empirical basis.
  Example (5-year horizon): "Full energy decarbonization + Current fossil dependency"

Rule 3: PHYSICAL/LOGICAL IMPOSSIBILITY
  Condition: Violates natural law, mathematical constraint, or tautological contradiction.
  Enforcement: Immediate exclusion; state the rule violated.
  Example: "Population growth + Population decline" (same variable, same period)

SCREENING PROTOCOL (apply in order):
  Step A: Check Rule 3 first → If violated: Exclude immediately, state contradiction
  Step B: Check Rule 1 → If violated: Exclude with causal mechanism explanation
  Step C: Check Rule 2 → If violated: Exclude with transition speed justification
  Step D: If no rules violated → Mark plausible = true

RESULT REPORTING:
  - List ALL excluded combinations with their Rule number
  - n_plausible = n_mathematical - n_excluded (computed by Python, not LLM)"""


# ── 6. 데모 / 자기 검증 ───────────────────────────────────────────────────────

def run_demo():
    sep = "=" * 60

    print(sep)
    print("DEMO 1: generate_combinations(n=2) — MITRE 2-axis (4 quadrants)")
    r = generate_combinations(2)
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 2: generate_combinations(n=4) — Defense Markets Thor (16 combos)")
    r = generate_combinations(4)
    # Print summary only for brevity
    print(json.dumps({
        "formula": r["formula"],
        "mathematical_total": r["mathematical_total"],
        "first_3_combos": r["combinations"][:3],
        "last_combo": r["combinations"][-1]
    }, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 3: validate_selection — PASS (4 selected from 4, 2-axis all plausible)")
    r = validate_selection(4, 0, 4, mode="default")
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 4: validate_selection — FAIL (3 selected, below minimum of 4)")
    r = validate_selection(4, 1, 3, mode="default")
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 5: validate_selection — PASS Defense Markets (6 from 13 plausible)")
    r = validate_selection(16, 3, 6, mode="defense_markets")
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 6: validate_selection — FAIL (7 selected, exceeds defense_markets max of 6)")
    r = validate_selection(16, 3, 7, mode="defense_markets")
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 7: generate_space — MITRE law enforcement 2-axis")
    axes = [
        {"name": "Funding", "driving_force": "Government Budget", "low": "Low", "high": "High"},
        {"name": "Attitudes", "driving_force": "Public Safety Policy", "low": "Permissive", "high": "Repressive"}
    ]
    r = generate_space(axes)
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 8: format_2axis_matrix — MITRE law enforcement case (verbatim names)")
    scenarios = [
        {"binary": [1, 1], "name": "Tough on Crime"},
        {"binary": [1, 0], "name": "Funded Permissiveness"},
        {"binary": [0, 1], "name": "Underfunded Crackdown"},
        {"binary": [0, 0], "name": "Neglect & Tolerance"}
    ]
    print(format_2axis_matrix(axes, scenarios))

    print(f"\n{sep}")
    print("DEMO 9: validate_selection — FAIL (duplicate axis names)")
    r = generate_space([
        {"name": "Funding", "driving_force": "Budget", "low": "Low", "high": "High"},
        {"name": "funding", "driving_force": "Budget", "low": "Low", "high": "High"}
    ])
    print(json.dumps(r, ensure_ascii=False, indent=2))

    print(f"\n{sep}")
    print("DEMO 10: exclusion_rules")
    print(describe_exclusion_rules())


# ── 7. CLI 진입점 ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic helper for vision-foresight-scenarios-scenario-logics-selection"
    )
    subparsers = parser.add_subparsers(dest="command")

    # generate_combinations
    p = subparsers.add_parser("generate_combinations", help="Generate all 2^n binary combinations")
    p.add_argument("n", type=int, help="Number of axes (2 <= n <= 6)")

    # validate_selection
    p = subparsers.add_parser("validate_selection", help="Validate 4-5 worlds selection rule")
    p.add_argument("n_mathematical", type=int, help="Total 2^n combinations")
    p.add_argument("n_excluded", type=int, help="Number excluded as implausible")
    p.add_argument("n_selected", type=int, help="Number of finally selected worlds")
    p.add_argument("--mode", default="default", choices=["default", "defense_markets"],
                   help="Selection mode: default=4-5 worlds, defense_markets=4-6 worlds")

    # generate_space
    p = subparsers.add_parser("generate_space", help="Generate full labeled scenario space")
    p.add_argument("axes_json", help="JSON array of axes: [{name, driving_force, low, high}, ...]")

    # format_matrix
    p = subparsers.add_parser("format_matrix", help="Format 2-axis MITRE markdown matrix")
    p.add_argument("axes_json", help="JSON array of exactly 2 axes")
    p.add_argument("scenarios_json", help="JSON array of scenarios: [{binary, name}, ...]")

    # exclusion_rules
    subparsers.add_parser("exclusion_rules", help="Print plausibility exclusion rules reference")

    # demo
    subparsers.add_parser("demo", help="Run self-test with built-in demo data")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == "demo":
            run_demo()
            sys.exit(0)

        elif args.command == "generate_combinations":
            result = generate_combinations(args.n)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0 if result.get("valid") else 1)

        elif args.command == "validate_selection":
            result = validate_selection(
                args.n_mathematical, args.n_excluded, args.n_selected, args.mode
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0 if result["valid"] else 1)

        elif args.command == "generate_space":
            axes = json.loads(args.axes_json)
            result = generate_space(axes)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(0 if result.get("valid") else 1)

        elif args.command == "format_matrix":
            axes = json.loads(args.axes_json)
            scenarios = json.loads(args.scenarios_json)
            print(format_2axis_matrix(axes, scenarios))
            sys.exit(0)

        elif args.command == "exclusion_rules":
            print(describe_exclusion_rules())
            sys.exit(0)

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)
