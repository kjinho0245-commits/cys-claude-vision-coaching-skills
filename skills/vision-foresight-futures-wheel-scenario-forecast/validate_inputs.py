#!/usr/bin/env python3
"""결정론적 입력 스키마 검증 — LLM 판단 대체.

Usage:
    python3 validate_inputs.py --input <path_to_json>

Exit codes:
    0 = valid
    1 = validation errors found
"""
import json
import sys
import argparse

VALID_SCENARIO_TYPES = {"optimistic", "pessimistic", "neutral", "driving_force", "custom"}
VALID_ITEM_TYPES = {"product", "technology", "policy", "organization", "service", "concept"}
VALID_PATTERNS = {"P1", "P2", "P3", "P4"}
VALID_CONTRADICTION_TYPES = {"logical", "empirical", "value"}
VALID_DF_STRENGTHS = {"high", "medium", "low"}


def validate_scenario(s: dict, idx: int = 0) -> list:
    errors = []
    prefix = f"scenarios[{idx}]"

    if not isinstance(s, dict):
        return [f"{prefix}: must be a dict"]

    if s.get("type") not in VALID_SCENARIO_TYPES:
        errors.append(
            f"{prefix}.type must be one of {sorted(VALID_SCENARIO_TYPES)}, got: {repr(s.get('type'))}"
        )

    name = s.get("name", "")
    if not name or not (1 <= len(str(name)) <= 100):
        errors.append(f"{prefix}.name required (1-100 chars), got: {repr(name)}")

    desc = s.get("description", "")
    if not desc or len(str(desc)) < 20:
        errors.append(
            f"{prefix}.description required (min 20 chars), got length: {len(str(desc))}"
        )

    dfs = s.get("driving_forces", [])
    if not isinstance(dfs, list) or not (2 <= len(dfs) <= 7):
        errors.append(
            f"{prefix}.driving_forces count must be 2-7, got {len(dfs) if isinstance(dfs, list) else 'non-list'}"
        )

    wsa = s.get("world_state_assumptions", [])
    if not isinstance(wsa, list) or len(wsa) < 2:
        errors.append(
            f"{prefix}.world_state_assumptions must have >= 2 items, got {len(wsa) if isinstance(wsa, list) else 'non-list'}"
        )

    return errors


def validate_item(item: dict) -> list:
    errors = []

    if not isinstance(item, dict):
        return ["item: must be a dict"]

    if not item.get("name"):
        errors.append("item.name required (non-empty string)")

    if item.get("type") not in VALID_ITEM_TYPES:
        errors.append(
            f"item.type must be one of {sorted(VALID_ITEM_TYPES)}, got: {repr(item.get('type'))}"
        )

    if not item.get("current_state"):
        errors.append("item.current_state required (non-empty string)")

    bf = item.get("baseline_features", [])
    if not isinstance(bf, list) or len(bf) < 2:
        errors.append(
            f"item.baseline_features must have >= 2 items, got {len(bf) if isinstance(bf, list) else 'non-list'}"
        )

    return errors


def validate_contradiction(cp: dict) -> list:
    errors = []
    for field in ["issue", "node_a", "node_b", "description"]:
        if not cp.get(field):
            errors.append(f"contradiction_promoted.{field} required for P4")
    ct = cp.get("contradiction_type")
    if ct not in VALID_CONTRADICTION_TYPES:
        errors.append(
            f"contradiction_promoted.contradiction_type must be one of {sorted(VALID_CONTRADICTION_TYPES)}, got: {repr(ct)}"
        )
    return errors


def validate_full(data: dict) -> list:
    errors = []

    pattern = data.get("pattern")
    if pattern not in VALID_PATTERNS:
        errors.append(
            f"pattern must be one of {sorted(VALID_PATTERNS)}, got: {repr(pattern)}"
        )
        return errors  # 이하 검증은 pattern 없으면 의미 없음

    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list) or len(scenarios) == 0:
        errors.append("scenarios: non-empty list required")
    else:
        for i, s in enumerate(scenarios):
            errors.extend(validate_scenario(s, i))

    if "item" not in data:
        errors.append("item: field required")
    else:
        errors.extend(validate_item(data["item"]))

    if pattern == "P4":
        cp = data.get("contradiction_promoted")
        if not cp or not isinstance(cp, dict):
            errors.append("P4 requires contradiction_promoted (dict)")
        else:
            errors.extend(validate_contradiction(cp))

    if pattern == "P2":
        # P2: driving_forces must be present in at least one scenario
        all_dfs = []
        for s in scenarios if isinstance(scenarios, list) else []:
            all_dfs.extend(s.get("driving_forces", []))
        if not all_dfs:
            errors.append("P2 requires at least one scenario with non-empty driving_forces")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic schema validator for vision-foresight-futures-wheel-scenario-forecast"
    )
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"valid": False, "errors": [f"File not found: {args.input}"]}))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"valid": False, "errors": [f"JSON parse error: {e}"]}))
        sys.exit(1)

    errors = validate_full(data)
    result = {"valid": len(errors) == 0, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
