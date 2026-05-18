#!/usr/bin/env python3
"""
vision-foresight-scenarios-leading-indicators — Deterministic Validator
결정론적 검증기: LLM이 자연어로 재추론하지 못하는 항목을 Python으로 강제 검증.

Usage:
  python3 validator.py --input li_data.json
  python3 validator.py --demo

Exit codes: 0=all valid, 1=errors found, 2=warnings only
"""

import json
import sys
import argparse
from typing import Any, Dict, List, Set, Tuple

# ── Constants ─────────────────────────────────────────────────────────────────

VALID_RHYTHMS = {"6-month", "quarterly", "monthly", "annual"}
VALID_INDICATOR_TYPES = {"quantitative", "qualitative"}
VALID_QUANTITATIVE_DIRECTIONS = {"↑", "↓", "↑↓"}
VALID_QUALITATIVE_DIRECTIONS = {"→", "↑", "↓", "↑↓"}

REQUIRED_TOP_KEYS = {
    "monitoring_rhythm",
    "scenarios",
    "alert_levels",
    "contingent_policy_linkage",
}
REQUIRED_SCENARIO_KEYS = {"id", "name", "indicators"}
REQUIRED_INDICATOR_KEYS = {"id", "name", "type", "current_value", "threshold", "direction", "source"}
REQUIRED_ALERT_KEYS = {"yellow", "orange", "red"}
REQUIRED_LINKAGE_KEYS = {"policy_id", "linked_indicator_ids", "activation_rule"}

INDICATOR_COUNT_MIN = 5
INDICATOR_COUNT_MAX = 15


# ── 1. Required sections check ────────────────────────────────────────────────

def check_required_sections(data: Dict) -> List[str]:
    errors = []
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"MISSING_SECTION: top-level key '{key}' absent")

    if "scenarios" in data:
        if not isinstance(data["scenarios"], list):
            errors.append("TYPE_ERROR: 'scenarios' must be a JSON array")
        else:
            for i, s in enumerate(data["scenarios"]):
                if not isinstance(s, dict):
                    errors.append(f"TYPE_ERROR: scenarios[{i}] must be a JSON object")
                    continue
                for k in REQUIRED_SCENARIO_KEYS:
                    if k not in s:
                        errors.append(f"MISSING_FIELD: scenarios[{i}] missing '{k}'")
                if "indicators" in s:
                    if not isinstance(s["indicators"], list):
                        errors.append(f"TYPE_ERROR: scenarios[{i}].indicators must be a JSON array")
                    else:
                        for j, ind in enumerate(s["indicators"]):
                            if not isinstance(ind, dict):
                                errors.append(f"TYPE_ERROR: scenarios[{i}].indicators[{j}] must be object")
                                continue
                            for k in REQUIRED_INDICATOR_KEYS:
                                if k not in ind:
                                    errors.append(
                                        f"MISSING_FIELD: scenarios[{i}].indicators[{j}] missing '{k}'"
                                    )

    if "alert_levels" in data:
        al = data["alert_levels"]
        if not isinstance(al, dict):
            errors.append("TYPE_ERROR: 'alert_levels' must be a JSON object")
        else:
            for k in REQUIRED_ALERT_KEYS:
                if k not in al:
                    errors.append(f"MISSING_FIELD: alert_levels missing '{k}'")

    if "contingent_policy_linkage" in data:
        cpl = data["contingent_policy_linkage"]
        if not isinstance(cpl, list):
            errors.append("TYPE_ERROR: 'contingent_policy_linkage' must be a JSON array")
        else:
            for i, link in enumerate(cpl):
                if not isinstance(link, dict):
                    errors.append(f"TYPE_ERROR: contingent_policy_linkage[{i}] must be object")
                    continue
                for k in REQUIRED_LINKAGE_KEYS:
                    if k not in link:
                        errors.append(f"MISSING_FIELD: contingent_policy_linkage[{i}] missing '{k}'")

    return errors


# ── 2. Scenario count check ───────────────────────────────────────────────────

def check_scenario_count(n: int) -> Tuple[str, str]:
    if n < 1:
        return "ERROR", "No scenarios provided"
    if n == 1:
        return "WARN", (
            "n=1: single scenario has no comparative signpost value. "
            "Z_Punkt verbatim: indicators help determine 'which direction of one or several scenarios'"
        )
    return "OK", f"n={n} scenarios"


# ── 3. Per-scenario indicator count ──────────────────────────────────────────

def check_indicator_count(scenario_id: str, n: int) -> Tuple[str, str]:
    """
    SKILL.md: 5-15 indicators per scenario.
    """
    if n < INDICATOR_COUNT_MIN:
        return "WARN", (
            f"Scenario '{scenario_id}' has n={n} indicators < {INDICATOR_COUNT_MIN} minimum. "
            f"SKILL.md requires {INDICATOR_COUNT_MIN}-{INDICATOR_COUNT_MAX} per scenario."
        )
    if n > INDICATOR_COUNT_MAX:
        return "WARN", (
            f"Scenario '{scenario_id}' has n={n} indicators > {INDICATOR_COUNT_MAX} maximum. "
            f"SKILL.md requires {INDICATOR_COUNT_MIN}-{INDICATOR_COUNT_MAX} per scenario."
        )
    return "OK", f"Scenario '{scenario_id}': n={n} indicators (within [{INDICATOR_COUNT_MIN},{INDICATOR_COUNT_MAX}])"


# ── 4. Indicator type check ───────────────────────────────────────────────────

def check_indicator_type(ind_id: str, type_val: Any) -> Tuple[bool, str]:
    if type_val not in VALID_INDICATOR_TYPES:
        return False, (
            f"TYPE_ERROR: Indicator '{ind_id}' type={type_val!r} "
            f"— must be 'quantitative' or 'qualitative'"
        )
    return True, ""


# ── 5. Direction consistency check ───────────────────────────────────────────

def check_direction(ind_id: str, direction: Any, ind_type: str) -> Tuple[bool, str]:
    """
    Quantitative: ↑, ↓, ↑↓  (numeric change)
    Qualitative: →, ↑, ↓, ↑↓  (state change or directional)
    """
    if ind_type == "quantitative" and direction not in VALID_QUANTITATIVE_DIRECTIONS:
        return False, (
            f"DIRECTION_ERROR: Indicator '{ind_id}' (quantitative) direction={direction!r} "
            f"— must be one of {sorted(VALID_QUANTITATIVE_DIRECTIONS)}"
        )
    if ind_type == "qualitative" and direction not in VALID_QUALITATIVE_DIRECTIONS:
        return False, (
            f"DIRECTION_ERROR: Indicator '{ind_id}' (qualitative) direction={direction!r} "
            f"— must be one of {sorted(VALID_QUALITATIVE_DIRECTIONS)}"
        )
    return True, ""


# ── 6. Threshold non-empty check ─────────────────────────────────────────────

def check_threshold(ind_id: str, threshold: Any) -> Tuple[bool, str]:
    """Threshold must be a non-empty string."""
    if threshold is None or (isinstance(threshold, str) and threshold.strip() == ""):
        return False, (
            f"THRESHOLD_EMPTY: Indicator '{ind_id}' has empty/null threshold. "
            f"Each indicator must define when it signals scenario emergence."
        )
    if not isinstance(threshold, str):
        return False, (
            f"THRESHOLD_TYPE: Indicator '{ind_id}' threshold={threshold!r} must be a string"
        )
    return True, ""


# ── 7. Monitoring rhythm check ───────────────────────────────────────────────

def check_monitoring_rhythm(rhythm: Any) -> Tuple[bool, str]:
    if rhythm not in VALID_RHYTHMS:
        return False, (
            f"RHYTHM_ERROR: monitoring_rhythm={rhythm!r} "
            f"— must be one of {sorted(VALID_RHYTHMS)}. "
            f"Z_Punkt verbatim DEFAULT is '6-month'."
        )
    return True, ""


# ── 8. Alert level consistency check ─────────────────────────────────────────

def check_alert_levels(al: Dict) -> List[str]:
    """
    yellow < orange < red (strictly increasing threshold counts).
    All must be positive integers ≥ 1.
    """
    errors = []
    y = al.get("yellow")
    o = al.get("orange")
    r = al.get("red")

    for name, val in [("yellow", y), ("orange", o), ("red", r)]:
        if not isinstance(val, int) or isinstance(val, bool) or val < 1:
            errors.append(
                f"ALERT_TYPE_ERROR: alert_levels.{name}={val!r} must be positive integer ≥ 1"
            )

    if all(isinstance(v, int) and not isinstance(v, bool) for v in [y, o, r]):
        if y >= o:
            errors.append(
                f"ALERT_ORDER_ERROR: yellow({y}) must be < orange({o})"
            )
        if o >= r:
            errors.append(
                f"ALERT_ORDER_ERROR: orange({o}) must be < red({r})"
            )

    return errors


# ── 9. Activation rule format check ──────────────────────────────────────────

def check_activation_rule(rule: Any, link_idx: int) -> Tuple[bool, str]:
    """
    Activation rule must be a non-empty string.
    Valid formats: "N/M", "all", "any", or descriptive string.
    """
    if rule is None or (isinstance(rule, str) and rule.strip() == ""):
        return False, (
            f"ACTIVATION_EMPTY: contingent_policy_linkage[{link_idx}].activation_rule is empty/null"
        )
    if not isinstance(rule, str):
        return False, (
            f"ACTIVATION_TYPE: contingent_policy_linkage[{link_idx}].activation_rule={rule!r} must be string"
        )
    return True, ""


# ── 10. Linked indicator ID existence check ──────────────────────────────────

def check_linked_indicators(
    link_idx: int,
    linked_ids: List,
    all_indicator_ids: Set[str],
) -> List[str]:
    """Each linked indicator ID must exist in the indicators list."""
    errors = []
    if not isinstance(linked_ids, list) or len(linked_ids) == 0:
        errors.append(
            f"LINKAGE_EMPTY: contingent_policy_linkage[{link_idx}].linked_indicator_ids is empty"
        )
        return errors
    for iid in linked_ids:
        if iid not in all_indicator_ids:
            errors.append(
                f"LINKAGE_UNKNOWN: contingent_policy_linkage[{link_idx}] references "
                f"indicator '{iid}' not found in any scenario"
            )
    return errors


# ── 11. Indicator ID uniqueness check ────────────────────────────────────────

def check_indicator_id_uniqueness(data: Dict) -> List[str]:
    """All indicator IDs across all scenarios must be globally unique."""
    errors = []
    seen = {}
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list):
        return errors
    for s in scenarios:
        if not isinstance(s, dict):
            continue
        for ind in s.get("indicators", []):
            if not isinstance(ind, dict):
                continue
            iid = ind.get("id")
            if iid is None:
                continue
            if iid in seen:
                errors.append(
                    f"DUPLICATE_ID: Indicator id='{iid}' appears in both "
                    f"scenario '{seen[iid]}' and scenario '{s.get('id', '?')}'"
                )
            else:
                seen[iid] = s.get("id", "?")
    return errors


# ── 12. Main validation orchestrator ─────────────────────────────────────────

def validate_li_output(data: Dict) -> Dict:
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Required sections
    errors.extend(check_required_sections(data))

    # 2. Monitoring rhythm
    if "monitoring_rhythm" in data:
        ok, msg = check_monitoring_rhythm(data["monitoring_rhythm"])
        if not ok:
            errors.append(msg)

    # 3. Alert levels
    if "alert_levels" in data and isinstance(data["alert_levels"], dict):
        errors.extend(check_alert_levels(data["alert_levels"]))

    # 4. Scenarios + indicators
    scenarios = data.get("scenarios", [])
    if isinstance(scenarios, list):
        n_s = len(scenarios)
        status, msg = check_scenario_count(n_s)
        if status == "ERROR":
            errors.append(f"COUNT_ERROR: {msg}")
        elif status == "WARN":
            warnings.append(f"COUNT_WARN: {msg}")

        for s in scenarios:
            if not isinstance(s, dict):
                continue
            sid = s.get("id", "?")
            indicators = s.get("indicators", [])
            if not isinstance(indicators, list):
                continue

            # Indicator count
            status, msg = check_indicator_count(sid, len(indicators))
            if status == "WARN":
                warnings.append(f"COUNT_WARN: {msg}")

            for ind in indicators:
                if not isinstance(ind, dict):
                    continue
                iid = ind.get("id", "?")
                ind_type = ind.get("type")

                # Type check
                if ind_type is not None:
                    ok, msg = check_indicator_type(iid, ind_type)
                    if not ok:
                        errors.append(msg)

                # Direction check
                direction = ind.get("direction")
                if ind_type in VALID_INDICATOR_TYPES and direction is not None:
                    ok, msg = check_direction(iid, direction, ind_type)
                    if not ok:
                        errors.append(msg)

                # Threshold check
                threshold = ind.get("threshold")
                ok, msg = check_threshold(iid, threshold)
                if not ok:
                    errors.append(msg)

                # Source non-empty check
                source = ind.get("source")
                if source is None or (isinstance(source, str) and source.strip() == ""):
                    warnings.append(
                        f"SOURCE_EMPTY: Indicator '{iid}' has empty source. "
                        f"Hallucination risk — source required for traceability."
                    )

    # 5. Indicator ID uniqueness
    errors.extend(check_indicator_id_uniqueness(data))

    # 6. Contingent policy linkage
    all_indicator_ids: Set[str] = set()
    if isinstance(scenarios, list):
        for s in scenarios:
            if isinstance(s, dict):
                for ind in s.get("indicators", []):
                    if isinstance(ind, dict) and "id" in ind:
                        all_indicator_ids.add(ind["id"])

    cpl = data.get("contingent_policy_linkage", [])
    if isinstance(cpl, list):
        for i, link in enumerate(cpl):
            if not isinstance(link, dict):
                continue
            rule = link.get("activation_rule")
            ok, msg = check_activation_rule(rule, i)
            if not ok:
                errors.append(msg)

            linked_ids = link.get("linked_indicator_ids", [])
            if all_indicator_ids:
                errors.extend(check_linked_indicators(i, linked_ids, all_indicator_ids))

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ── 13. Demo / self-test ──────────────────────────────────────────────────────

DEMO_VALID = {
    "monitoring_rhythm": "6-month",
    "scenarios": [
        {
            "id": "S1",
            "name": "AGI Boom",
            "indicators": [
                {"id": "I01", "name": "AI Patent Applications", "type": "quantitative",
                 "current_value": "450K/year", "threshold": "> 900K/year",
                 "direction": "↑", "source": "WIPO Patent Database"},
                {"id": "I02", "name": "AGI Benchmark Pass", "type": "qualitative",
                 "current_value": "None", "threshold": "Public claim by top-5 lab",
                 "direction": "→", "source": "Lab announcements / peer review"},
                {"id": "I03", "name": "AI R&D Investment", "type": "quantitative",
                 "current_value": "$90B/yr", "threshold": "> $200B/yr",
                 "direction": "↑", "source": "IEA / Stanford AI Index"},
                {"id": "I04", "name": "AI Firm Market Cap Share", "type": "quantitative",
                 "current_value": "8%", "threshold": "> 20% of S&P500",
                 "direction": "↑", "source": "Bloomberg/Reuters"},
                {"id": "I05", "name": "Government AI Strategy", "type": "qualitative",
                 "current_value": "35 nations", "threshold": "≥ 100 nations with dedicated AI law",
                 "direction": "→", "source": "OECD AI Policy Observatory"}
            ]
        },
        {
            "id": "S2",
            "name": "Regulation World",
            "indicators": [
                {"id": "I06", "name": "AI Regulatory Bills", "type": "quantitative",
                 "current_value": "12/year globally", "threshold": "> 50 binding laws enacted",
                 "direction": "↑", "source": "OECD/IAPP regulatory tracker"},
                {"id": "I07", "name": "AI Incident Registry", "type": "quantitative",
                 "current_value": "340/year", "threshold": "> 1000/year OR 1 mass-casualty event",
                 "direction": "↑", "source": "AIAAIC incident database"},
                {"id": "I08", "name": "AI Market Concentration", "type": "quantitative",
                 "current_value": "HHI 2400", "threshold": "HHI > 3500 in AI services",
                 "direction": "↑", "source": "DOJ/EC competition reports"},
                {"id": "I09", "name": "Civil Society AI Protests", "type": "qualitative",
                 "current_value": "< 5 major events/year", "threshold": "> 20 events involving > 100K people",
                 "direction": "→", "source": "Media monitoring / GDELT"},
                {"id": "I10", "name": "AI Ethics Standards Adoption", "type": "qualitative",
                 "current_value": "ISO/IEC 42001 drafted", "threshold": "Mandatory ISO AI compliance in G7",
                 "direction": "→", "source": "ISO/IEC SC 42 Working Group"}
            ]
        }
    ],
    "alert_levels": {
        "yellow": 1,
        "orange": 3,
        "red": 5
    },
    "contingent_policy_linkage": [
        {
            "policy_id": "CP01",
            "policy_name": "Emergency AI Reskilling Program",
            "linked_indicator_ids": ["I01", "I03", "I07"],
            "activation_rule": "2/3 crossed"
        },
        {
            "policy_id": "CP02",
            "policy_name": "AI Safety Moratorium",
            "linked_indicator_ids": ["I02", "I07"],
            "activation_rule": "any crossed"
        }
    ]
}

DEMO_INVALID = {
    "monitoring_rhythm": "weekly",
    "scenarios": [
        {
            "id": "S1",
            "name": "Test",
            "indicators": [
                {"id": "I01", "name": "X", "type": "bad_type",
                 "current_value": "5", "threshold": "",
                 "direction": "up", "source": ""},
                {"id": "I01", "name": "Y", "type": "quantitative",
                 "current_value": "5", "threshold": "> 10",
                 "direction": "↑", "source": "source1"}
            ]
        }
    ],
    "alert_levels": {
        "yellow": 3,
        "orange": 1,
        "red": -2
    },
    "contingent_policy_linkage": [
        {
            "policy_id": "CP01",
            "linked_indicator_ids": ["I99"],
            "activation_rule": ""
        }
    ]
}


def run_demo():
    print("=== DEMO: Valid output ===")
    r = validate_li_output(DEMO_VALID)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()
    print("=== DEMO: Invalid output (multiple errors) ===")
    r2 = validate_li_output(DEMO_INVALID)
    print(json.dumps(r2, ensure_ascii=False, indent=2))


# ── 14. CLI entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic validator for vision-foresight-scenarios-leading-indicators JSON"
    )
    parser.add_argument("--input", help="Path to LI JSON file")
    parser.add_argument("--demo", action="store_true", help="Run self-test with demo data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(2)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    result = validate_li_output(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["valid"]:
        sys.exit(1)
    elif result["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)
